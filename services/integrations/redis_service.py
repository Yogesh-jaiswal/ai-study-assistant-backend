import app.extensions as ext

def set_key(key: str, value: str, ttl: int | None = None) -> None:
    """
    Maps the redis key with the value and also sets ttl if given.

    Args:
        key: Redis key
        value: Value to store
        ttl: Expiration in seconds
    """

    if ttl is not None:
        ext.redis_client.set(name=key, value=value, ex=ttl)
    else:
        ext.redis_client.set(name=key, value=value)

def get_key(key: str) -> str | None:
    """
    Get the value by key.
    """
    return ext.redis_client.get(key)

def delete_key(key: str) -> int:
    """
    Delete the key from Redis.
    """
    return ext.redis_client.delete(key)

def exists(key: str) -> bool:
    """
    Checks if key exists in Redis DB.
    """
    return bool(ext.redis_client.exists(key))

def ttl(key: str) -> int:
    """
    Returns the time to live for a key.
    """
    return ext.redis_client.ttl(key)

def expire(key: str, ttl: int) -> bool:
    """
    Adds ttl to already existing key.
    """
    return bool(ext.redis_client.expire(key, ttl))