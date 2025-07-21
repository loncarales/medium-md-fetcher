"""
URL collection utilities for CLI
"""

import re
from typing import List, Tuple

from rich import print as rprint
from rich.prompt import Prompt


def collect_urls_interactive() -> List[str]:
    """
    Collect URLs interactively from user input
    Based on the provided click example but using the rich for better UX
    """
    urls = []

    rprint("[bold blue]Enter Medium URLs one by one.[/bold blue]")
    rprint("[dim]Press Enter on an empty line to finish, or type 'q' to quit.[/dim]\n")

    while True:
        try:
            url = Prompt.ask(f"URL #{len(urls) + 1}", default="", show_default=False)

            # Check for quit command
            if url.lower() in ["q", "quit", "exit"]:
                break

            # Check for empty input (finish)
            if not url.strip():
                break

            urls.append(url.strip())

            # Visual confirmation
            if is_medium_url(url.strip()):
                rprint(f"[green]✓[/green] Added: {url.strip()}")
            else:
                rprint(f"[yellow]⚠[/yellow] Added (might not be a Medium URL): {url.strip()}")

        except KeyboardInterrupt:
            rprint("\n[yellow]Input cancelled by user[/yellow]")
            break

    if urls:
        rprint(f"\n[green]Collected {len(urls)} URLs:[/green]")
        for i, url in enumerate(urls, 1):
            rprint(f"  {i}. {url}")
    else:
        rprint("\n[yellow]No URLs collected.[/yellow]")

    return urls


def validate_medium_urls(urls: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate a list of URLs and separate valid Medium URLs from invalid ones

    Args:
        urls: List of URLs to validate

    Returns:
        Tuple of (valid_urls, invalid_urls)
    """
    valid_urls = []
    invalid_urls = []

    for url in urls:
        if is_medium_url(url):
            valid_urls.append(url)
        else:
            invalid_urls.append(url)

    return valid_urls, invalid_urls


def is_medium_url(url: str) -> bool:
    """
    Check if a URL is a valid Medium article URL

    Args:
        url: URL to validate

    Returns:
        True if URL appears to be a Medium article URL
    """
    medium_patterns = [
        r"https?://medium\.com/@[\w-]+/[\w-]+",  # medium.com/@author/article
        r"https?://[\w-]+\.medium\.com/[\w-]+",  # subdomain.medium.com/article
        r"https?://medium\.com/[\w-]+/[\w-]+",  # medium.com/publication/article
        r"https?://[\w-]+\.com/[\w-]+.*medium",  # Custom domain with medium
    ]

    return any(re.match(pattern, url, re.IGNORECASE) for pattern in medium_patterns)
