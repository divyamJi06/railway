import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
DEBUG = True

LOGIN_URL= '/auth/signin'
ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', 'web-production-44bc.up.railway.app' , "https://web-production-44bc.up.railway.app"]

CSRF_TRUSTED_ORIGINS = ["https://web-production-44bc.up.railway.app"]

# Application definition

INSTALLED_APPS = [
    'bilti',
    'user',


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['bilti/templates/bilti',
        'user/templates/user'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
import os
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'bilti/static/'), 
       os.path.join(BASE_DIR, 'bilti/static/'),
    #    os.path.join(BASE_DIR, 'user/static/'),
]

STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('DB_NAME'),
    'USER' : os.environ.get('DB_USER'),
    'PASSWORD' : os.environ.get('DB_PASSWORD'),
    'HOST' : os.environ.get('DB_HOST'),
    'PORT' : 5432
}
}
if not DEBUG:
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


USER_DETAILS={
    
                "name": "MGT CARGO",
                "address": "H. NO 119A, NEAR KALI MANDIR, JP ROAD, HARHARGUTTU, BAGBERA, JAMSHEDPUR, EAST SINGHBHUM",
                "phone": "0987654321",
                "sac": "",
                "email": "mgtcargo@gmail.com",
                "pan": "AKPPG5749H",
                "gst": "20AKPPG5749HIAB",
                "bank_name": "AXIS BANK",
                "bank_ifsc": "123456789012345",
                "bank_acno": "ICIC0000160"
}
