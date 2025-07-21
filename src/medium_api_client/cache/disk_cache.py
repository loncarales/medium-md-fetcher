"""
DiskCache based cache implementation
"""

from typing import Any, Dict, Optional

from diskcache import Cache

from .base import CacheInterface


class DiskCache(CacheInterface):
    def __init__(self, db_path: str = "/tmp"):
        self.db_path = db_path
        self.cache = self.init_db()

    def init_db(self):
        return Cache(self.db_path)

    def get(self, key: str) -> Optional[Dict[Any, Any]]:
        return self.cache.get(key)

    def set(self, key: str, value: Dict[Any, Any], ttl: int = 3600) -> bool:
        return self.cache.set(key, value)  # default None, no expiry

    def delete(self, key: str) -> bool:
        return self.cache.delete(key)

    def close(self):
        self.cache.close()
