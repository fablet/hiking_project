from base import *  # noqa

SECRET_KEY = r"{{ secret_key }}"


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hiking_test',
        'USER': 'django',
        'PASSWORD': 'xxx',
        'HOST': '127.0.0.1',
    }
}

ADMINS = (
    ('Fable', 'fable@raintechpdx.com'),
)
INSTALLED_APPS += (
    'core',
)
