import os
from datetime import timedelta
import mimetypes
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, ".env.dev"))

mimetypes.add_type("text/css", ".css", True)


DEBUG = os.getenv("DEBUG")


# Env vars for self site backend
SECRET_KEY = os.getenv("SECRET_KEY")
MAIN_HOST_SCHEME = os.environ.get("MAIN_HOST_SCHEME")
MAIN_HOST = os.environ.get("MAIN_HOST")

WHERE_IS_MEDIA_ROOT = os.getenv("WHERE_IS_MEDIA_ROOT")

FRONTEND_URL = f"{MAIN_HOST_SCHEME}://{os.getenv('FRONTEND_URL')}"
SITE_URL = f"{MAIN_HOST_SCHEME}://{MAIN_HOST}"
ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_PORT = os.getenv("ELASTIC_PORT")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX")
ELASTIC_URL = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}/{ELASTIC_INDEX}/_search"
ELASTIC_URL_INSERT = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"


SECRET_KEY = os.getenv("SECRET_KEY")

VUE_DEV = os.getenv("VUE_DEV")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

FROM_EMAIL_ADMIN = f"PartsHub Admin <mikohan1@gmail.com>"

# SECURITY WARNING: don't run with debug turned on in production!


PRODUCT_DESCRIPTION = "Материлы изготовления: сталь, алюминий, резина, стекло, пластик. Произведена на высокоточном оборудовании, с соблюдением всех допусков."

# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "192.168.0.107",
#     "192.168.0.109",
#     "192.168.0.24",
#     "46.151.155.97",
#     "dnobaka.ru",
#     "localhost",
#     "partshub.tk",
#     "angara77.ru",
#     "0.0.0.0",
#     "angara77.ml",
#     "angara77.ga",
#     "django",
# ]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

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

HOST = os.environ.get("MYSQL_HOST")


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

ONE_C_PRICE_DIR = os.getenv("ONE_C_PRICE_DIR")
ONE_C_PRICE = os.path.join(BASE_DIR, ONE_C_PRICE_DIR)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "front/dist"),
    # os.path.join(BASE_DIR, "media"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
SHARED_DATA = os.path.join(
    BASE_DIR,
    "shared_data",
)

if WHERE_IS_MEDIA_ROOT == "local":
    MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
    SHARED_DATA = os.path.join(
        BASE_DIR,
        "..",
        "shared_data",
    )


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
EMAIL_MANAGERS = ["angara99@gmail.com", "angara77@gmail.com", "yellkalolka@gmail.com"]

# Email for technical information mostly from crontab
EMAIL_ADMINS = ["angara99@gmail.com", "yellkalolka@gmail.com"]

EMAIL_REPLY_TO = ["angara77@gmail.com"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.sendinblue.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
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

### From local settings


YM_CREDENTIALS = {
    "PARTSHUB": {
        "OAUTH": os.getenv("YANDEX_MARKET_PARTSHUB_TOKEN"),
        "CAMPAIGN_ID": os.getenv("YANDEX_MARKET_PARTSHUB_ID"),
    },
    "ANGARA": {
        "OAUTH": os.getenv("YANDEX_MARKET_ANGARA_TOKEN"),
        "CAMPAIGN_ID": os.getenv("YANDEX_MARKET_ANGARA_ID"),
    },
}


OAUTH_OZON = os.getenv("OAUTH_OZON")
OZON_ID = os.getenv("OZON_ID")


YANDEX_MARKET_TOKEN = os.getenv("YANDEX_MARKET_TOKEN")


PHOTO_FOLDER_FOR_CHECK = "/home/manhee/SMB/0_ANGARA_PRO_PHOTO/all_photo"
PHOTO_FOLDER_FOR_AGES = "/home/manhee/Pictures/parts"

VUE_DEV = os.getenv("VUE_DEV")


EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


SOCIAL_SECRET = os.getenv("SOCIAL_SECRET")


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

CURRENCY_LATEST_URL = os.getenv("CURRENCY_LATEST_URL")


# ONE_C_PRICE = "/home/manhee/backend/quora/test_category/all.csv"

# CRONJOBS = [
#     (
#         "5 3 * * *",
#         "product.syncronizators.products_sync.sync_products",
#     ),
#     (
#         "0 4 * * *",
#         "test_category.elastic_insert.do_all_two",
#     ),
#     (
#         "0 5 * * *",
#         "test_category.elastic_stuff2.do_insert",
#     ),
#     (
#         "50 4 * * *",
#         "product.syncronizators.prices_sync.update_prices",
#     ),
#     (
#         "*/20 * * * *",
#         "orders.check_site.check",
#     ),
# ]
