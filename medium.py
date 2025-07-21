"""
Main CLI entry point for a Medium API client
"""

import logging

import click
from dotenv import load_dotenv
from rich import print as rprint
from rich.console import Console
from rich.logging import RichHandler

from src.cli.commands.download import download
from src.medium_api_client.cache.disk_cache import DiskCache
from src.medium_api_client.client import MediumAPIClient


load_dotenv()
console = Console()

# Configure the root logger
logging.basicConfig(
    level="INFO",  # Set your desired logging level
    format="%(message)s",  # RichHandler handles its own formatting, but a simple format is needed
    datefmt="[%X]",  # Time format for RichHandler
    handlers=[
        RichHandler(
            # console=console, # Pass your custom console if you created one
            show_level=True,
            show_time=True,
            rich_tracebacks=True,  # Enable rich tracebacks
            tracebacks_theme="monokai",  # Choose a traceback theme
            tracebacks_word_wrap=True,
            log_time_format="%Y-%m-%d %H:%M:%S",  # Custom timestamp format
        )
    ],
)

logger = logging.getLogger(__name__)  # Get your module-specific logger


@click.group()
@click.option("--api-key", envvar="RAPIDAPI_KEY", help="RAPIDAPI_KEY environment variable")
@click.option("--cache-path", default="data/cache", help="Cache database path")
@click.option("--articles-path", default="data/articles", help="Saved articles path")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def cli(ctx, api_key, cache_path, articles_path, verbose):
    """Medium API CLI - Access Medium articles programmatically"""
    if not api_key:
        rprint("[red]Error: API key is required. Set RAPIDAPI_KEY environment variable or use --api-key option[/red]")
        ctx.exit(1)

    # Initialize cache
    cache = DiskCache(db_path=cache_path)

    # Create client
    client = MediumAPIClient(api_key=api_key, cache=cache, logger=logger)

    # Store in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["client"] = client
    ctx.obj["console"] = console
    ctx.obj["logger"] = logger
    ctx.obj["articles_path"] = articles_path
    ctx.obj["verbose"] = verbose


# Register commands
cli.add_command(download)

if __name__ == "__main__":
    cli()
