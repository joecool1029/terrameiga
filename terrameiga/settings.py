#¡¡¡¡¡¡¡¡¡¡¡¡  SETTINGS DEPLOYMENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""
Django settings for terrameiga project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print ("ruta do BASE_DIR", BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q=m#etp8+mf8)iu!a7+xs!*0$pc5j@_c5ndt^u77$vwq8+jwvc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*'] 

#Esto é para que non me de error a hora de completar os formularios no móbil ou no ordenador nin en ningún outro dispositivo, e para poder acceder o admin site sen problema.
CSRF_TRUSTED_ORIGINS = ['https://terrameiga.bike', 'https://*.terrameiga.bike', 'https://terrameiga-production.up.railway.app', 'https://terrameiga-production.up.railway.app*']
CSRF_COOKIE_SECURE = False

#Variable para activar o framework das alerts de django

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'products',
    'bicicleteiros',
    'tools',
    'newsletter',
    #Esto é para o rich text
    'ckeditor',
    #Amazon Web Service Storage
    'storages',
    #ESto é para que aparezan os puntos nos datos dos países e os números sexan máis visibles
    'django.contrib.humanize',

]
# This is to indicate to Django that the user model is now this custom model (CustomeUser) instead of the User model
#IMPORTANTE! No caso de que "python manage.py migrate" non che funcione, referencialo a app que sexa.
# Algo como "python manage.py migrate registration"
AUTH_USER_MODEL = 'registration.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #Esto é para detectar o idioma do usuario e que a páxina se moster no idioma que ten configurado
    #Se o non tes o idioma do usuario mostraráse o inglés por defecto
    # LocaleMiddleware tries to determine the users language preference by following this algorithm:
    # First, it looks for a django_language key in the current users session.
    # Failing that, it looks for a cookie called django_language .
    # Failing that, it looks at the Accept-Language HTTP header. This header is sent by your browser and tells the server which language(s) you prefer, in order of priority. Django tries each language in the header until it finds one with available translations.
    # Failing that, it uses the global LANGUAGE_CODE setting.
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'terrameiga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #Indicamos onde temos os templates para que os vaia a buscar
        'DIRS': [BASE_DIR / 'terrameiga/static/templates/',
                 BASE_DIR / 'registration/static/templates/',
                 BASE_DIR / 'bicicleteiros/static/templates/',
                 BASE_DIR / 'tools/static/templates/',
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

WSGI_APPLICATION = 'terrameiga.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PGNAME'),
        'PGUSER': config('PGUSER'), 
        'PGPASSWORD': config('PGPASSWORD'),
        'PGHOST': config('PGHOST'), 
        'PGPORT': config('PGPORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://www.vitainbeta.org/how-to-install-homebrew-on-mac-linux-windows/
# https://docs.djangoproject.com/en/4.1/topics/i18n/
# To make the site available in other languages you have to install the gettext package following the video you have recorded
# https://www.youtube.com/watch?v=eMI2mE8rG5w
# Then run "python manage.py makemessages -l es" to create the .po file fot (in this case) Spanish as you can see at the end of the command "es"
# Then go to .po file and translate the text
# Then run the following command "python manage.py compilemessages" and the .mo file will be created.
# Then, if you change the language code to a language that you have made the translation, all the web, as well as the alerts will be transalated to the language you chose
# However, MIDDLEWARE, there is 'django.middleware.locale.LocaleMiddleware', which detects the language of the browser and put the webiste in the same language
# as the browser.
#COMO FUNCIONA O IDIOMA NA TÚA PÁXINA: IMPORTANTE - LÓXICA QUE APLICO
#As urls https:terrameiga/en/ ou https:terrameiga/es mostraranse cada unha delas dependendo do idioma que teña configurado o user no browser.
#Non obstante, se o usuario selecciona outra opción de idioma na home_page_nonregsitered (footer), o idioma do usuario modificarase no campo do language do modelo CustomUser e todas
#as urls pasaran a estar no idioma que o user seleccionou, independientemente do idioma que teña configurado o user no browser.
#Tamén, se o usuario vai a personal_data e decide cambiar o idioma, as urls modificaranse de acorde ao idioma que seleccione o usuario, independentemente do idioma que teña o usuario
#no browser
#OUTRA COUSA DO IDIOMA ENTRE O IDIOMA NO SIGN_IN E O SIGN_UP
#No Sign_up gardo o idioma que está na url (que se cargou en fución do idiomado browser), nos datos do usuario, porque entendo que é o que quere utlizar.
#No sign_in utilizo o idioma que o usuario ten na súa configuración. O usuario pode ter o browser en Español, pero se nas súas preferencias ten galeo, a páxina tras o sign_in estará en galego

#Estes son os idiomas que vamos a permitir que a xente escolla. Solo é para lle dar a xente a opción de escoller.
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('gl', _('Galician')),
    ('ca', _('Catalan')),
    ('eu', _('Basque')),
    ]
#Language code is the defalut languages which is used when nothing is specified.
LANGUAGE_CODE = 'en-us'

#ESto é para o tema de ter múltiples idiomas na páxina web.
LOCALE_PATHS = [
   os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#IMPORTANTE: o STATICFILES_DIRS é para indicar onde metes os arquivos estáticos. Ollo, non ten nada que ver con templates
#A ruta aos templates indícase arriba no "TEMPLATES" para que vaia a buscar os templates.
STATICFILES_DIRS=[
   BASE_DIR / "terrameiga/static/"
]

#Esto é para asignarlle un sitio a carpeta que se crea cando se fai o "python manage.py collectstatic"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATIC FILES - Telo que facer así tal cual, porque senon non che vai a funcionar
AWS_S3_CUSTOM_DOMAIN = 'terrameiga.s3.eu-west-3.amazonaws.com/staticfiles'  # Specify your custom domain here
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#MEDIA FILES: Estes son arquivos que subo ou suben a app os usuarios e que se van a gardar no bucket de terrameiga en S3 que se chama: "media_files".
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'terrameiga'
AWS_S3_FILE_OVERWRITE = True #Quero que cando se suba un arquivo co mesmo nome este se reemplace"
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#SMTP Configuration para envío de emails
# https://www.youtube.com/watch?v=sFPcd6myZrY
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')





