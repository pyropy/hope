from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "hope"
VERSION = "1.0.0"
API_PREFIX = "/api"

# CDN
CDN_ACCESS_KEY_ID = config("CDN_ACCESS_KEY_ID", cast=str)
CDN_SECRET_ACCESS_KEY = config("CDN_SECRET_ACCESS_KEY", cast=str) 
CDN_ENDPOINT_URL = config("CDN_ENDPOINT_URL", cast=str)
CDN_LINK_LIFESPAN = config("CDN_LINK_LIFESPAN_SECONDS", cast=int, default=7 * 24 * 60 * 60) # age in seconds NOTE: Max alowed 7 days

SECRET_KEY = config("SECRET_KEY", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
  "ACCESS_TOKEN_EXPIRE_MINUTES",
  cast=int,
  default=7 * 24 * 60 #one week
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="mpei-kids:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

# POSTGRES
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
