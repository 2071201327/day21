import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'zhangxiao')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'day21')
    MYSQL_CHARSET = 'utf8'
    
    REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_ENCODING = 'utf8'
    
    DB_POOL_MAX_CONNECTIONS = int(os.environ.get('DB_POOL_MAX_CONNECTIONS', 50))
    DB_POOL_MIN_CACHED = int(os.environ.get('DB_POOL_MIN_CACHED', 5))
    DB_POOL_MAX_CACHED = int(os.environ.get('DB_POOL_MAX_CACHED', 20))
    
    REDIS_POOL_MAX_CONNECTIONS = int(os.environ.get('REDIS_POOL_MAX_CONNECTIONS', 1000))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
