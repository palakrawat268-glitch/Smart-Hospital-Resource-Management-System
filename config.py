import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hospital-secret-key-prod-random-token-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MySQL Database Configuration
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'hospital_db')
    
    # Toggle SQLite fallback for easy development/testing if MySQL isn't configured
    USE_SQLITE = os.environ.get('USE_SQLITE', 'false').lower() in ('true', '1', 'yes')

    @classmethod
    def get_database_uri(cls):
        custom_url = os.environ.get('DATABASE_URL')
        if custom_url:
            return custom_url
        if cls.USE_SQLITE:
            instance_dir = os.path.join(BASE_DIR, 'instance')
            os.makedirs(instance_dir, exist_ok=True)
            return f"sqlite:///{os.path.join(instance_dir, 'hospital.db')}"
        return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DB}?charset=utf8mb4"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    USE_SQLITE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
