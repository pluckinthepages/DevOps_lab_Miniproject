"""Environment-driven configuration for CampusFind."""
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///campusfind.db")
    PORT = int(os.environ.get("PORT", "5000"))
    VERSION = "1.0.0"
    ITEMS_PER_PAGE = 9
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret-key"


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name=None):
    return CONFIGS.get(name or os.environ.get("FLASK_ENV", "production"), ProductionConfig)
