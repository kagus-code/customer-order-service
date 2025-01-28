from .base import *  # noqa

DEBUG = True

# add your development host here
ALLOWED_HOSTS += ["*"]  # noqa

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True


CORS_ALLOWED_ORIGIN_REGEXES = (
    r"^(https?:\/\/)?((localhost)|(127\.0\.0\.1)):\d{4}"
)
