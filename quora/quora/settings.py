import os
from .local_settings import *
from datetime import timedelta
import mimetypes
mimetypes.add_type("text/css", ".css", True)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = False

if os.environ.get('DJANGO_DEBUG') and os.environ.get('DJANGO_DEBUG') == 'True':
    DEBUG = True

MAIN_HOST = 'localhost:8080'

MAIN_HOST_SSL = 'http'
if os.environ.get('MAIN_HOST_SSL'):
    MAIN_HOST_SSL = 'https'

if os.environ.get('MAIN_HOST'):
    MAIN_HOST = os.environ.get('MAIN_HOST')


if os.environ.get('ELASTIC_HOST'):
    ELASTIC_URL = f"{os.environ.get('ELASTIC_HOST')}:9200"
else:
    ELASTIC_URL = "localhost:9200"

ELASTIC_INDEX = "prod_all"


SECRET_KEY = SECRET_KEY
VUE_DEV = VUE_DEV

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

FROM_EMAIL_ADMIN = f"PartsHub Admin <mikohan1@gmail.com>"

# SECURITY WARNING: don't run with debug turned on in production!


PRODUCT_DESCRIPTION = "Материлы изготовления: сталь, алюминий, резина, стекло, пластик. Произведена на высокоточном оборудовании, с соблюдением всех допусков."

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.0.107",
    "192.168.0.109",
    "192.168.0.24",
    "46.151.155.97",
    "dnobaka.ru",
    "localhost",
    "partshub.tk",
    "angara77.ru",
    "0.0.0.0",
    "angara77.ml",
    "angara77.ga",
    "django",
]


# Default images folder for blog posts and categories
BLOG_IMAGES = "blog/images"
CAR_IMAGES = "images/cars"
USER_IMAGES = "images/users"
CATEGORY_IMAGES = "images/categories"

# Default Author for blog articles
DEFAULT_AUTHOR = "Team of PartsHub.ru"

# Folder to find photos ready for uploading

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "mathfilters",
    "django_extensions",
    "mptt",
    "django_mptt_admin",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    "corsheaders",
    # "rest_auth",
    # "rest_auth.registration",
    "crispy_forms",
    "ckeditor",
    "ckeditor_uploader",
    "webpack_loader",
    "bootstrap_pagination",
    "users",
    "home",
    "brands",
    "brand_dict",
    "product",
    "blog",
    "test_category",
    "vasya_interface",
    "graphene_django",
    "company_pages",
    "taggit",
    "drf_yasg",
    "django_crontab",
    ####################
    "authentication",
    "social_auth",
    "orders",
    "stats",
    "yandex_market",
]


MIDDLEWARE = [
    #        'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "quora.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "front/dist"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "product.context_processor.session_processor",
                "quora.context_processor.main_host",
            ],
        },
    },
]


WSGI_APPLICATION = "quora.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get("MYSQL_HOST"):
    HOST = os.environ.get("MYSQL_HOST")
else:
    HOST = "127.0.0.1"


DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #    },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": HOST,
        "OPTIONS": {
            "read_default_file": os.path.join(BASE_DIR, "quora/my.cnf"),
            "sql_mode": "traditional",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


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

# MAX UPLOAD DATA
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Price for product update
# ONE_C_PRICE = os.path.join(BASE_DIR, "test_category/all.csv")
ONE_C_PRICE = os.path.join(BASE_DIR, "..", "shared_data/all.csv")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "front/dist"),
    # os.path.join(BASE_DIR, "media"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")

MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_collection")

# CKEDITOR_BASEPATH = os.path.join(STATIC_ROOT, "ckeditor")
CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"

# django crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# django.contrib.sites
SITE_ID = 1

# django-allauth
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False


# CORS Configuration
CORS_ORIGIN_ALLOW_ALL = True


# Django-REST-Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "dist/",
        "STATS_FILE": os.path.join(BASE_DIR, "front", "webpack-stats.json"),
    }
}

AUTH_USER_MODEL = "users.CustomUser"

COMPANY_INFO = {
    "phone": "8-800-200-99-53",
    "email": "angara77@gmail.com",
    "website": FRONTEND_URL,
}
EMAIL_MANAGERS = ["angara99@gmail.com",
                  "angara77@gmail.com", "yellkalolka@gmail.com"]

# Email for technical information mostly from crontab
EMAIL_ADMINS = ["angara99@gmail.com", "yellkalolka@gmail.com"]

EMAIL_REPLY_TO = ["angara77@gmail.com"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_USE_TLS = True

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=300),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=10),
}
