"""
Memory-based cache implementation for unit testing
"""

import time
from typing import Any, Dict, Optional

from src.medium_api_client.cache.base import CacheInterface


class MemoryCache(CacheInterface):
    def __init__(self):
        self.cache: Dict[str, Dict[Any, Any]] = {}

    def get(self, key: str) -> Optional[Dict[Any, Any]]:
        """
        Retrieves a value from the memory cache by its key.
        Checks for expiration. If expired, deletes the item and returns None.
        Returns None if the key is not found or has expired.
        """
        item = self.cache.get(key)
        if item is None:
            # print(f"DEBUG: Get '{key}' - Not found.")
            return None

        current_time = int(time.time())
        expires_at = item.get("expires_at", 0)  # Default to 0 if not set (e.g., old entries)

        if 0 < expires_at <= current_time:
            # Item has expired
            print(f"DEBUG: Get '{key}' - Expired. Deleting.")
            self.delete(key)  # Remove the expired item
            return None
        else:
            # Item is valid
            print(f"DEBUG: Get '{key}' - Found and valid.")
            return item["value"]

    def set(self, key: str, value: Dict[Any, Any], ttl: int = 3600) -> bool:
        """
        Sets a key-value pair in the memory cache with a Time-To-Live (TTL).
        'Ttl' is in seconds.
        Returns True indicating success.
        """
        # Calculate expiration timestamp. Use 0 for no expiration if ttl is <= 0.
        expires_at = int(time.time()) + ttl if ttl > 0 else 0

        self.cache[key] = {"value": value, "expires_at": expires_at}
        return True

    def delete(self, key: str) -> bool:
        """
        Deletes a key-value pair from the memory cache.
        Returns True if the key was found and deleted, False otherwise.
        """
        if key in self.cache:
            del self.cache[key]
            print(f"DEBUG: Deleted '{key}'.")
            return True
        print(f"DEBUG: Delete '{key}' - Not found.")
        return False

    def close(self):
        """
        Clears the memory cache, effectively resetting it.
        This is useful for ensuring a clean state between unit tests.
        """
        self.cache.clear()
