DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3'...
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'exo_messages',
        'USER': 'postgres',
        'PASSWORD': 'su82jr',
        'HOST': 'localhost',
        'PORT': '5434',
    }
}
