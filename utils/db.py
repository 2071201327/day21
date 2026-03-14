import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors
import logging
from utils.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Pool = PooledDB(
    creator=pymysql,
    maxconnections=Config.DB_POOL_MAX_CONNECTIONS,
    mincached=Config.DB_POOL_MIN_CACHED,
    maxcached=Config.DB_POOL_MAX_CACHED,
    blocking=True,
    setsession=[],
    ping=0,
    host=Config.MYSQL_HOST,
    port=Config.MYSQL_PORT,
    user=Config.MYSQL_USER,
    passwd=Config.MYSQL_PASSWORD,
    charset=Config.MYSQL_CHARSET,
    db=Config.MYSQL_DATABASE
)

def fetch_one(sql, params):
    conn = None
    cursor = None
    try:
        conn = Pool.connection()
        cursor = conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql, params)
        result = cursor.fetchone()
        logger.info(f"fetch_one executed: {sql}")
        return result
    except Exception as e:
        logger.error(f"fetch_one error: {e}, sql: {sql}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_all(sql, params):
    conn = None
    cursor = None
    try:
        conn = Pool.connection()
        cursor = conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        logger.info(f"fetch_all executed: {sql}")
        return result
    except Exception as e:
        logger.error(f"fetch_all error: {e}, sql: {sql}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert(sql, params):
    conn = None
    cursor = None
    try:
        conn = Pool.connection()
        cursor = conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql, params)
        conn.commit()
        last_id = cursor.lastrowid
        logger.info(f"insert executed: {sql}")
        return last_id
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"insert error: {e}, sql: {sql}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute(sql, params):
    conn = None
    cursor = None
    try:
        conn = Pool.connection()
        cursor = conn.cursor(cursor=cursors.DictCursor)
        cursor.execute(sql, params)
        conn.commit()
        logger.info(f"execute executed: {sql}")
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"execute error: {e}, sql: {sql}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
