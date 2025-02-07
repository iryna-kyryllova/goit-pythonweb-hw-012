import redis.asyncio as redis
import json
from typing import Optional
from sqlalchemy.orm import class_mapper
from datetime import datetime
from src.database.models import User
from src.conf.config import settings


class RedisCache:
    """
    Service for caching user data in Redis.
    """

    def __init__(self):
        """
        Initialize Redis connection.
        """
        self.redis = None

    async def connect(self):
        """
        Establish connection with Redis.
        """
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )

    async def set_user(self, user: User, ttl: int = 3600):
        """
        Cache the user data in Redis.

        Args:
            user: User object to cache.
            ttl: Time to live for the cache (default: 1 hour).
        """
        user_data = {
            column.key: getattr(user, column.key)
            for column in class_mapper(User).columns
        }

        for key, value in user_data.items():
            if isinstance(value, datetime):
                user_data[key] = value.isoformat()

        user_json = json.dumps(user_data)

        await self.redis.set(f"user:{user.id}", user_json, ex=ttl)

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve user from Redis cache.

        Args:
            user_id: ID of the user.

        Returns:
            User object if found, otherwise None.
        """
        user_data = await self.redis.get(f"user:{user_id}")
        if user_data:
            try:
                user_dict = json.loads(user_data)
                user_dict["id"] = int(user_dict["id"])
                return User(**user_dict)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Помилка читання кешу для user_id={user_id}: {e}")
        return None

    async def delete_user(self, user_id: int):
        """
        Remove user from cache.

        Args:
            user_id: ID of the user to delete from cache.
        """
        await self.redis.delete(f"user:{user_id}")


cache = RedisCache()
