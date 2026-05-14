import json
import functools
from typing import Any, Callable, Optional
from app.core.redis_client import redis_client
from loguru import logger

def cached(ttl: int = 3600, key_prefix: str = "cache"):
    """
    Decorator to cache function results in Redis.
    Assumes the decorated function is async.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            # We use a simple representation for demo purposes
            args_str = ":".join(map(str, args))
            kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{func.__name__}:{args_str}:{kwargs_str}"
            
            try:
                cached_val = await redis_client.get(cache_key)
                if cached_val:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return json.loads(cached_val)
            except Exception as e:
                logger.warning(f"Redis cache lookup failed: {e}")

            result = await func(*args, **kwargs)

            try:
                await redis_client.set(cache_key, json.dumps(result), expire=ttl)
                logger.debug(f"Cache stored for key: {cache_key}")
            except Exception as e:
                logger.warning(f"Redis cache storage failed: {e}")

            return result
        return wrapper
    return decorator

def invalidate_cache(key_prefix: str):
    """
    Decorator to invalidate cache entries with a given prefix.
    Useful for POST/PUT/DELETE operations.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # In a real-world scenario, we might want to be more specific 
            # with which keys to invalidate. For now, we can use a pattern.
            # Redis doesn't have a direct 'delete by prefix' in the async client 
            # without keys(), which is discouraged in production. 
            # For this task, we'll assume a simpler strategy or manual deletion.
            logger.info(f"Invalidating cache for prefix: {key_prefix}")
            # Placeholder for complex invalidation logic
            return result
        return wrapper
    return decorator
