"""
Abstract base class for cache implementations
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Dict[Any, Any]]:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Dict[Any, Any], ttl: int = 3600) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
