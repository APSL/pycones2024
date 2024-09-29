import logging.config
from datetime import timedelta
from pathlib import Path

from configurations import Configuration

from main.config import Config

config = Config("app.ini", "app.local.ini")

# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = config.get("Security", "SECRET_KEY")
    DEBUG = config.get("Debug", "DEBUG", False)
    ENABLE_DEBUG_TOOLBAR = config.get("Debug", "ENABLE_DEBUG_TOOLBAR", False) and DEBUG

    ALLOWED_HOSTS = config.get("Security", "ALLOWED_HOSTS")

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # third parties
        "django_extensions",
        "rest_framework",
        "drf_spectacular",
        "knox",
        # apps
        "main",
        "core.apps.CoreConfig",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "main.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "main.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/4.2/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/

    STATIC_ROOT = config.get("Paths", "STATIC_ROOT")
    STATIC_URL = config.get("Paths", "STATIC_URL", "static/")

    MEDIA_ROOT = config.get("Paths", "MEDIA_ROOT")
    MEDIA_URL = config.get("Paths", "MEDIA_URL", "media/")

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    @property
    def LOGGING(self):  # noqa
        res = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": config.get(
                        "Logs", "LOG_FORMATTER_FORMAT", "[%(asctime)s] %(levelname)s %(name)s-%(lineno)s %(message)s"
                    ),
                }
            },
            "filters": {
                "require_debug_false": {
                    "()": "django.utils.log.RequireDebugFalse",
                }
            },
            "handlers": {
                "default": {
                    "level": config.get("Logs", "LOG_LEVEL", "WARNING"),
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "loggers": {
                "default": {
                    "handlers": ["default"],
                    "level": config.get("Logs", "LOG_LEVEL", "WARNING"),
                    "propagate": False,
                },
                "requests.packages.urllib3": {
                    "handlers": ["default"],
                    "level": config.get("Logs", "LOG_LEVEL", "WARNING"),
                    "propagate": False,
                },
                "django": {
                    "handlers": ["default"],
                    "level": config.get("Logs", "DJANGO_LOG_LEVEL", "WARNING"),
                    "propagate": False,
                },
            },
        }
        extra_logging_ = config.get("Logs", "EXTRA_LOGGING", "")
        if extra_logging_:
            for extra_ in extra_logging_.split(","):
                module, level = extra_.split(":")
                res["loggers"][module] = {
                    "handlers": ["default"],
                    "level": level,
                    "propagate": False,
                }
        logging.config.dictConfig(res)
        return res

    if ENABLE_DEBUG_TOOLBAR:
        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
        INTERNAL_IPS = ["127.0.0.1"]

    REST_KNOX = {
        "SECURE_HASH_ALGORITHM": config.get("Authentication", "SECURE_HASH_ALGORITHM", "hashlib.sha512"),
        "AUTH_TOKEN_CHARACTER_LENGTH": config.get("Authentication", "AUTH_TOKEN_CHARACTER_LENGTH", "64"),
        "TOKEN_TTL": timedelta(minutes=config.get("Authentication", "TOKEN_TTL_IN_MINUTES", 600)),
        "USER_SERIALIZER": "knox.serializers.UserSerializer",
        "TOKEN_LIMIT_PER_USER": config.get("Authentication", "TOKEN_LIMIT_PER_USER", None),
        "AUTO_REFRESH": config.get("Authentication", "AUTO_REFRESH", False),
        "MIN_REFRESH_INTERVAL": config.get("Authentication", "MIN_REFRESH_INTERVAL_IN_SECONDS", 60),
        "TOKEN_MODEL": "knox.AuthToken",
    }
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # drf-spectacular
    }

    # docs https://drf-spectacular.readthedocs.io/en/latest/settings.html
    SPECTACULAR_SETTINGS = {
        "TITLE": config.get("Api", "SPECTACULAR_TITLE", "OpenAPI"),
        "DESCRIPTION": config.get("Api", "SPECTACULAR_DESCRIPTION", ""),
        "VERSION": config.get("Api", "SPECTACULAR_VERSION", "0.0.1"),
        "SERVE_INCLUDE_SCHEMA": config.get("Api", "SPECTACULAR_SERVE_INCLUDE_SCHEMA", False),
        "SCHEMA_PATH_PREFIX": "/(api|auth)",
    }


class Test(Base):
    pass
