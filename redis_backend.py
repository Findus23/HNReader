from aredis import StrictRedis
from ratelimit.backends.redis import RedisBackend, DECREASE_SCRIPT


# noinspection PyMissingConstructor
class CustomRedisBackend(RedisBackend):
    def __init__(
            self,
            r: StrictRedis
    ) -> None:
        self._redis = r
        self.decrease_function = self._redis.register_script(DECREASE_SCRIPT)
