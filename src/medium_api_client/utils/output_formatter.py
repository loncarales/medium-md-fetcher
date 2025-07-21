"""
Output formatting utilities for CLI
"""

from typing import List

from rich.table import Table

from src.medium_api_client.models import Article


def format_article_table(articles: List[Article]) -> Table:
    """
    Format articles as a rich table for console display

    Args:
        articles: List of article dictionaries

    Returns:
        Rich Table object
    """
    table = Table(title="Downloaded Articles", show_header=True, header_style="bold magenta")

    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="bold")
    table.add_column("Tags", style="cyan")
    table.add_column("Topics", style="green")
    table.add_column("Published", justify="right", style="yellow")

    for i, article in enumerate(articles, 1):
        table.add_row(
            str(i),
            article.title,
            ", ".join(article.tags) if article.topics else "N/A",
            ", ".join(article.topics) if article.topics else "N/A",
            article.published_at.strftime("%Y-%m-%d %H:%M:%S") if article.published_at else "N/A",
        )

    return table


def save_articles_md(articles: List[Article], output_dir: str) -> Table:
    """
    Save articles as Markdown files in the specified directory

    Args:
        articles: List of Article objects
        output_dir: Directory to save Markdown files

    Returns:
        Rich Table object with file paths
    """
    table = Table(title="Saved Articles", show_header=True, header_style="bold magenta")

    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="bold")
    table.add_column("File Path", style="cyan")

    for i, article in enumerate(articles, 1):
        file_path = f"{output_dir}/{article.unique_slug}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(article.markdown)

        table.add_row(str(i), article.title, file_path)

    return table
