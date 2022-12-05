from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("JTRO_SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ.get('JTRO_ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
    'drf_yasg',
]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if os.environ.get('JTRO_DEV_DATABASE') == "postgis":
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('JTRO_DEV_DATABASE_ENGINE'),
            'NAME': os.environ.get('JTRO_DEV_DATABASE_NAME'),
            'USER': os.environ.get('JTRO_DEV_DATABASE_USER'),
            'PASSWORD': os.environ.get('JTRO_DEV_DATABASE_PASSWORD'),
            'HOST': os.environ.get('JTRO_DEV_DATABASE_HOST'),
            'PORT': os.environ.get('JTRO_DEV_DATABASE_PORT'),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

SWAGGER_SETTINGS = {
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
}

try:
    from .local import *
except ImportError:
    pass
