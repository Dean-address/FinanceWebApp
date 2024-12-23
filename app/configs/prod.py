from .base import *
from decouple import config
import dj_database_url

DEBUG = config("DEBUG")
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "dean-finance.up.railway.app"]

CSRF_TRUSTED_ORIGIN = ["https://dean-finance.up.railway.app"]

DATABASES = {
    "default": dj_database_url.parse(config("DB_URL")),
}
