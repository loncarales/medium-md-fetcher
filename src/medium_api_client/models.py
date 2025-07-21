"""
Data models and Pydantic schemas
Contains: Article
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Article(BaseModel):
    """
    Represents a Medium article.
    """

    id: str
    title: str
    subtitle: str | None
    author: str
    published_at: datetime = None
    last_modified_at: datetime = None
    markdown: Optional[str] = None
    tags: List[str] = []
    topics: List[str] = []
    url: str
    unique_slug: str
    is_locked: bool = False
