"""
Download command for Medium articles
"""

import time

import click
from rich import print as rprint
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from src.cli.utils.url_collector import collect_urls_interactive, validate_medium_urls
from src.medium_api_client.exceptions import MediumAPIException
from src.medium_api_client.utils.output_formatter import format_article_table, save_articles_md


@click.command()
@click.option("--urls", "-u", multiple=True, help="Medium URLs to download (can be used multiple times)")
@click.option("--file", "-f", type=click.File("r"), help="File containing URLs (one per line)")
@click.option("--interactive", "-i", is_flag=True, help="Interactive URL input")
@click.pass_context
def download(ctx, urls, file, interactive):
    """Download Medium articles from provided URLs"""
    client = ctx.obj["client"]
    console = ctx.obj["console"]
    verbose = ctx.obj["verbose"]

    # Collect URLs from various sources
    url_list = []

    # From command line arguments
    if urls:
        url_list.extend(urls)

    # From file
    if file:
        url_list.extend([line.strip() for line in file if line.strip()])

    # Interactive input
    if interactive or not url_list:
        interactive_urls = collect_urls_interactive()
        url_list.extend(interactive_urls)

    if not url_list:
        rprint("[red]No URLs provided. Use --interactive, --urls, or --file options.[/red]")
        ctx.exit(1)

    # Validate URLs
    valid_urls, invalid_urls = validate_medium_urls(url_list)

    if invalid_urls:
        rprint(f"[yellow]Warning: {len(invalid_urls)} invalid URLs found:[/yellow]")
        for url in invalid_urls:
            rprint(f"  - {url}")

    if not valid_urls:
        rprint("[red]No valid Medium URLs found.[/red]")
        ctx.exit(1)

    # Get articles from valid URLs
    # They will be downloaded one by one or fetch from cache
    # TODO: Implement concurrent downloads | asynchronous processing
    articles = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        description = f"Downloading '{len(valid_urls)}' article(s) from Medium"
        task = progress.add_task(description, total=len(valid_urls))
        time.sleep(1)

        for i, url in enumerate(valid_urls, 1):
            try:
                progress.update(task, description=f"Downloading article {i}/{len(valid_urls)}")
                article = client.get_article_by_url(url)
                if article:
                    articles.append(article)
                    if verbose:
                        rprint(f"[green]✓ Downloaded: {article.title}[/green]")
                else:
                    if verbose:
                        rprint(f"[red]✗ Failed to download: {url}[/red]")

                progress.update(task, advance=1)

            except MediumAPIException as e:
                if verbose:
                    rprint(f"[red]✗ Error downloading {url}: {str(e)}[/red]")
                progress.update(task, advance=1)
                continue

    # Display results
    if articles:
        rprint(f"\n[green]Successfully downloaded {len(articles)} articles[/green]")

        table = format_article_table(articles)
        console.print(table)

        table = save_articles_md(articles, ctx.obj["articles_path"])
        console.print(table)
