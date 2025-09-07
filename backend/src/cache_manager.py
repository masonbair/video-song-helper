import time
import threading
from typing import Dict, Any, Optional

# Simple in-memory cache with TTL support
class CacheManager:
    def __init__(self, default_ttl_seconds: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl_seconds
        self.lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key in self.cache:
                cache_item = self.cache[key]
                # Check if item has expired
                if cache_item["expires_at"] > time.time():
                    return cache_item["data"]
                else:
                    # Clean up expired item
                    del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expires_at = time.time() + ttl
        
        with self.lock:
            self.cache[key] = {
                "data": data,
                "expires_at": expires_at
            }
    
    def delete(self, key: str) -> None:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self) -> None:
        with self.lock:
            self.cache.clear()

# Create a global instance
cache = CacheManager()
