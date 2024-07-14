from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import pymongo


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")


DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "lendsqr-backend.vercel.app",
    "adedddccccedf4f10b8aa1c2c9d31cdd-1391532181.eu-north-1.elb.amazonaws.com",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lendsqr",
    "rest_framework",
    "djoser",
    "corsheaders",
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'user_details',
#         'USER': config('DB_USER'),
#         'PASSWORD': config('PASSWORD'),
#         'HOST': config('HOST'),
#         'PORT': 3306,
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# need to pass as env in dockerfile from jenkins
db_user = os.getenv("DB_USER")
db_password = os.getenv("PASSWORD")
db_cluster = os.getenv("CLUSTERNAME")

MONGO_CLIENT = pymongo.MongoClient(
    f"mongodb+srv://{db_user}:{db_password}@{db_cluster}.jzsljb4.mongodb.net/?retryWrites=true&w=majority"
)
MONGO_DB = MONGO_CLIENT["user_details"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": os.getenv("AUTH_PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": 52687,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://{os.getenv("REDIS")}:6379/1",
        "LOCATION": f"redis://localhost:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "example",
    }
}

CACHE_TTL = 60 * 2

GRIDFS_STORAGE_DB = "user_details"
GRIDFS_STORAGE_COLLECTION = "images"


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


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}


DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": False,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    # 'ACTIVATION_URL': 'activate/{uid}/{token}',
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user_create": "lendsqr.serializers.UserCreateSerializer",
        "user": "lendsqr.serializers.UserCreateSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Toronto"


USE_I18N = True

USE_TZ = True


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "shawenmedia"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = "public-read"


AWS_LOCATION = "staticfiles"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
DEFAULT_FILE_STORAGE = "backend.storages.MediaStore"


MEDIA_DIR = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIA_URL = "/media/"
# MEDIA_URL = os.path.join(BASE_DIR, 'media')

CORS_ORIGIN_WHITELIST = [
    "https://oluwaseun-johnson-lendsqr-fe-test.netlify.app",
    "https://lendsqr-backend.vercel.app",
    "http://localhost:3000",
    "https://a150f97ebbba34795aa15c75de625aff-569107307.eu-north-1.elb.amazonaws.com",
]

AUTH_USER_MODEL = "lendsqr.User"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
