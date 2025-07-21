"""
Basic usage example for Medium API client
"""
import os
from src.medium_api_client.client import MediumAPIClient


def main():
    # Load API key from environment
    api_key = os.getenv('MEDIUM_API_KEY')
    if not api_key:
        print("Please set MEDIUM_API_KEY environment variable")
        return

    # Create client
    client = MediumAPIClient(api_key=api_key)

    # Example usage
    article_url = "https://medium.com/@author/article-title-123abc"
    article = client.get_article_by_url(article_url)

    if article:
        print(f"Title: {article.title}")
        print(f"Author: {article.author}")
    else:
        print("Article not found")


if __name__ == "__main__":
    main()
