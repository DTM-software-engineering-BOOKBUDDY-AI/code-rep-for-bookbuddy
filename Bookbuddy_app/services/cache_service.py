from functools import wraps
from datetime import datetime, timedelta
import json
import os

class CacheService:
    def __init__(self, cache_dir='cache', expiry_hours=24):
        self.cache_dir = cache_dir
        self.expiry_hours = expiry_hours
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key):
        try:
            cache_path = self._get_cache_path(key)
            if not os.path.exists(cache_path):
                return None
            
            with open(cache_path, 'r') as f:
                data = json.load(f)
            
            # Check if cache has expired
            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=self.expiry_hours):
                os.remove(cache_path)
                return None
            
            return data['value']
        except Exception:
            return None
    
    def set(self, key, value):
        try:
            cache_path = self._get_cache_path(key)
            data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

# Decorator for caching
def cache_result(expiry_hours=24):
    def decorator(func):
        cache_service = CacheService(expiry_hours=expiry_hours)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Try to get from cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # If not in cache, call function and cache result
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result)
            return result
        
        return wrapper
    return decorator 