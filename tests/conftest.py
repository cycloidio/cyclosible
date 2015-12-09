import os


def pytest_configure():
    from django.conf import settings

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        BASE_DIR=BASE_DIR,
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.locale.LocaleMiddleware',
        ),
        ROOT_URLCONF='cyclosible.Cyclosible.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
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
        ],
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'cyclosible.Cyclosible',
            'guardian',
            'cyclosible.playbook',
            'cyclosible.appversion',
            'rest_framework',
            'rest_framework_swagger',
            'rest_framework.authtoken',
            'djcelery',
            'tests',
        ),
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        AUTHENTICATION_BACKENDS=(
            'django.contrib.auth.backends.ModelBackend',  # default
            'guardian.backends.ObjectPermissionBackend',
        ),
        REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
            'PAGE_SIZE': 10,
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.BasicAuthentication',
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.TokenAuthentication',
            ),
            'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)

        },
        ANONYMOUS_USER_ID=-1,
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0',
        CELERY_TIMEZONE='Europe/Paris',
        CELERY_ALWAYS_EAGER=True,
        TEST_RUNNER='djcelery.contrib.test_runner.CeleryTestSuiteRunner',
        WS4REDIS_SUBSCRIBER='cyclosible.Cyclosible.websocket.WebSocketSubscriber',
        WS4REDIS_PREFIX='ws',
        WS4REDIS_EXPIRE=7200,
        WS4REDIS_CONNECTION={
            'host': 'localhost',
            'port': 6379,
            'db': 1,
        }
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
