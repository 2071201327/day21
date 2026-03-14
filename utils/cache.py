import redis
from utils.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POOL = redis.ConnectionPool(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    encoding=Config.REDIS_ENCODING,
    max_connections=Config.REDIS_POOL_MAX_CONNECTIONS
)

def push_queue(value):
    conn = None
    try:
        conn = redis.Redis(connection_pool=POOL)
        conn.lpush("DAY21_TASK_QUEUE", value)
        logger.info(f"pushed to queue: {value}")
    except Exception as e:
        logger.error(f"push_queue error: {e}")
        raise
    finally:
        if conn:
            conn.close()
