from pathlib import Path

# ======== BASE DIRECTORY ========
BASE_DIR = Path(__file__).resolve().parent.parent


# ======== SECURITY SETTINGS ========
SECRET_KEY = 'django-insecure-5lq5s+gxqyve$f3_tcjvaisz+#+i63y!zj^j!t3%2n!-4+#@k8'
DEBUG = True
ALLOWED_HOSTS = ["192.168.1.7", "10.0.2.2", "localhost", "127.0.0.1", "*","192.168.1.6"]  # dev


# ======== APPLICATIONS ========
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    'corsheaders',
    "rest_framework_simplejwt.token_blacklist",

    # Local apps
    'depot',
    "accounts",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": False,
}




# ======== MIDDLEWARE ========
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # harus paling atas (di atas CommonMiddleware)
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======== URL & WSGI ========
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# ======== TEMPLATES ========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ======== DATABASE ========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ======== PASSWORD VALIDATION ========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ======== INTERNATIONALIZATION ========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ======== STATIC FILES ========
STATIC_URL = 'static/'


# ======== DEFAULT PRIMARY KEY ========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======== CORS CONFIG (izinkan semua origin) ========
CORS_ALLOW_ALL_ORIGINS = True
