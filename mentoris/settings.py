"""
Django settings for mentoris project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pbmmo011$5_b^69e9k-#1#)i8)*!n)io8-y0rz=@&e6@h7s!zk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "mentapp",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "multiupload",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mentoris.urls"

# Locations checked for templates may look a little strange,
# but, this is needed to work on Elastic Beanstalk
TEMPLATES = [
    {
<<<<<<< HEAD
        "BACKEND": "django.template.backends.django.DjangoTemplates",
<<<<<<< HEAD
        "DIRS": ["mentoris/templates"],
=======
        "DIRS": [
            "mentoris/templates",
<<<<<<< HEAD
            "mentapp/templates,",
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
            "mentoris/mentoris/templates/mentapp",
>>>>>>> 7a8d51f (Fixed misc bugs related to deployment and formatting for the quiz display)
=======
=======
=======
            "mentapp/templates",
>>>>>>> ce5099f (Update settings.py)
            os.path.join(settings.BASE_DIR, "/mentoris/templates/"),
>>>>>>> 12eb4a2 (Update settings.py to fix missing templates in deployment)
=======
            os.path.join(settings.BASE_DIR, "/mentoris/templates/"),
>>>>>>> 62669bb (Fixed Deployment missing template sign up)
            os.path.join(settings.BASE_DIR, "/mentoris/templates/mentapp"),
>>>>>>> 5445009 (Fixed template not found bug on AWS)
        ],
>>>>>>> d759b0b (Linux bug fix)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
=======
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['mentoris/templates', 'mentapp/templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
>>>>>>> b1d7166 (Fixed loading landing.html and volume.html)
            ],
        },
    },
]


WSGI_APPLICATION = "mentoris.wsgi.application"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
DATABASES = {
<<<<<<< HEAD
       
=======
=======
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
>>>>>>> 1c5155a (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
=======
=======
# DATABASES = {
# }

>>>>>>> 489da96 (Changed admin page to use email plus implemented custom user model in app)
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
DATABASES = {
<<<<<<< HEAD
<<<<<<< HEAD
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
=======
=======
>>>>>>> f94ffd3 (Issues with model definitions)
=======
DATABASES = {
>>>>>>> 7ea149b (Changes for routing)
=======
DATABASES = {
>>>>>>> a9ea21b (Working Logout Button, picture for logout button might be nice)
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mentoris',
        'USER': 'walden',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 489da96 (Changed admin page to use email plus implemented custom user model in app)
=======
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mentoris",
        "USER": "jpark",
        "PASSWORD": "pass4Janice",
        "HOST": "localhost",
        "PORT": "5432",
>>>>>>> 54d7931 (Fixed Email Routing)
    }
}
=======
DATABASES = {}
>>>>>>> 58b0f25 (Remove DB)

<<<<<<< HEAD
>>>>>>> a8bcbf5 (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))

<<<<<<< HEAD

DATABASES = {

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> aabf7f6 (edit/delete quiz buttons)
}
=======
DATABASES = {

=======
>>>>>>> 472b9a9 (edit buttons redirect)
=======
        
>>>>>>> 03d532c (page render with question info, latex not saving to db)
=======
       
>>>>>>> 469f2d9 (create question, redirect to edit page)
=======
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
>>>>>>> 17d417d (Answer Keys and Rubrics)
=======
DATABASES = {}
>>>>>>> 68755a4 (Update settings.py)
=======
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "helloworld",
    }
}
=======
DATABASES = {}
>>>>>>> 05075fd (Update settings.py)

>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
=======
    }
}
>>>>>>> 7ea149b (Changes for routing)
=======
    }
}
>>>>>>> a9ea21b (Working Logout Button, picture for logout button might be nice)


}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

>>>>>>> d0301e5 (fixed quiz deletion bug)
=======
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

<<<<<<< HEAD
DATABASES = {

 
}

>>>>>>> 1d1ddb5 (edit question functionality)
=======
DATABASES = {}
>>>>>>> e5984d8 (Implement Email Verification & Password Reset)

<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
DATABASES = {
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        'default': {
=======
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

<<<<<<< HEAD
DATABASES = {
}
>>>>>>> 32cac51 (Associated Quiz Feedback to Quiz instead of Rendering)
=======
DATABASES = {}
>>>>>>> 7916013 (Implemented Question Approval Page)
=======
    }
}
>>>>>>> f94ffd3 (Issues with model definitions)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
=======
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
=======
>>>>>>> 721fa8e (stylesheet quotes)
=======
>>>>>>> 7a8d51f (Fixed misc bugs related to deployment and formatting for the quiz display)

=======
DATABASES = {
}
>>>>>>> 32653f4 (Added Texlive distribution)

<<<<<<< HEAD
>>>>>>> 6684e51 (Display question attachments implemented, needed to add MEDIA_URL and MEDIA_ROOT in settings.py and modify urls.py to serve user created images.)

<<<<<<< HEAD
        'NAME': 'mentoris',

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        'USER': 'ashton',

        'PASSWORD': 'postgreshton',
=======
        'USER': 'postgres',

        'PASSWORD': 'pass4Janice',
>>>>>>> bc27416 (Implemented Sign Up Page Front End)
=======
        'USER': 'walden',

        'PASSWORD': '',
>>>>>>> f3cec87 (Added Sign Up Form Validation and Multi-Select Dropdown for other Languages)
=======
        'USER': 'ashton',

        'PASSWORD': 'postgreshton',
>>>>>>> f3a6090 (profile page)
=======
        'USER': 'walden',

        'PASSWORD': '',
>>>>>>> 0e05ba7 (fixed db credentials)

        'HOST': 'localhost',

        'PORT': '',
        }
=======
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "mentoris",
        "USER": "walden",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
=======
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
>>>>>>> 4b3c7bd (Added email to models.py)
=======
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
>>>>>>> 48995dc (Added functionality to sign_up page)
=======
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
>>>>>>> 0b5462f (Implemented Request Translation Email Notification)
    }
>>>>>>> 6502796 (Merged in changes from sign up page)
=======
             'PASSWORD': '',

             'HOST': 'localhost',
      }
>>>>>>> b1d7166 (Fixed loading landing.html and volume.html)
=======
        'USER': 'muser',
=======
        'USER': 'Walden',
>>>>>>> a8a49c7 (Fixed credentials)

        'PASSWORD': '',
=======
        'USER': 'ashton',

        'PASSWORD': 'postgreshton',
>>>>>>> 91d40a5 (Able to populate fields from db)
=======
        'USER': 'walden',

        'PASSWORD': '',
>>>>>>> 64f1aeb (db credentials)

        'HOST': 'localhost',

        'PORT': '5432',
        }
>>>>>>> 398700d (Fixed identation in settings.py)
=======
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'MentappMentorispasSCars2ElasticStalkBean!',
    #     'HOST': 'mentorisdb.cmkrvc9icttm.us-west-2.rds.amazonaws.com',
    #     'PORT': '5432',
    #     }
=======
>>>>>>> 7e08393 (Update settings.py)

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mentoris',
        'USER': 'walden',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        }
>>>>>>> b473aa5 (added tables)
=======
   #Local db

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 7fc2710 (main page volume + chapter selector)
=======
    # Local db
>>>>>>> 17adf3a (Implemented the Chapter Page with Quiz Information)
=======
   #Local db

>>>>>>> dc9408a (update)
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'mentoris',
    #     'USER': 'ashton',
    #     'PASSWORD': 'postgreshton',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    #     }
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'mentoris',
    #     'USER': 'walden',
    #     'PASSWORD': '',
    #     'HOST': 'localhost',
    #     'PORT': '5432',
    # }
=======
=======
>>>>>>> 906fe04 (download works)
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mentoris',
        'USER': 'walden',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        }
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> da1caf7 (behind)

    #Production db

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'MentappMentorispasSCars2ElasticStalkBean!',
    #     'HOST': 'mentorisdb.cmkrvc9icttm.us-west-2.rds.amazonaws.com',
    #     'PORT': '5432',
    #     }
=======

  
    
>>>>>>> 7fc2710 (main page volume + chapter selector)

=======
>>>>>>> 17adf3a (Implemented the Chapter Page with Quiz Information)
=======
=======
>>>>>>> 906fe04 (download works)

    #Production db

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'MentappMentorispasSCars2ElasticStalkBean!',
    #     'HOST': 'mentorisdb.cmkrvc9icttm.us-west-2.rds.amazonaws.com',
    #     'PORT': '5432',
    #     }
=======
>>>>>>> 3771c88 (Update settings.py)
    
=======

>>>>>>> c02fa63 (Fixed minor syntax error)

>>>>>>> dc9408a (update)
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
<<<<<<< HEAD
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
=======
=======
DATABASES = {
     

=======
DATABASES = {     
<<<<<<< HEAD
>>>>>>> 52968c0 (Implemented User Directory and Promotion Page)
=======

    
        
>>>>>>> e813f48 (add attachments and blobs to db)
    # "default": {
    #      "ENGINE": "django.db.backends.sqlite3",
    #      "NAME": BASE_DIR / "db.sqlite3",
    # }
}
>>>>>>> 0f02bac (Fixed volume filtering)
=======

>>>>>>> 207f103 (Fixed LaTex page, fixed arrows discovered it was a cache issue, styled edit quiz and edit quiz add question pages)

>>>>>>> f354f38 (edit quiz page, added header and footer html files, and colors css file)
=======
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'MentappMentorispasSCars2ElasticStalkBean!',
        'HOST': 'mentorisdb.cmkrvc9icttm.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
        }
>>>>>>> e2a52bd (fixed form submission)
}
=======
=======
>>>>>>> 0f14dbf (view supports)

>>>>>>> 2eb3b9f (misc change)
=======

>>>>>>> c02fa63 (Fixed minor syntax error)
=======
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mentoris',
        'USER': 'walden',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
>>>>>>> 7192f3b (quiz render grabs quizzes from DB)
=======
DATABASES = {}
>>>>>>> c1333c2 (Remove DB)
=======
DATABASES = {}
>>>>>>> 1c2c15d (rm db)
=======
DATABASES = {}
>>>>>>> bca0a50 (RM DB)

=======
>>>>>>> 2fb46dc (Removed Database)

=======
>>>>>>> 1bfca8f (Replaced Django form with custom form, removed a redundant variable and made changes to styling)
=======

>>>>>>> 0ae4eb6 (Merging Base Feedback w/ Main)
=======
>>>>>>> 66d0926 (Removed log and print statements, fixed quiz name in chapter.html)
=======

>>>>>>> 62669bb (Fixed Deployment missing template sign up)
=======
>>>>>>> a84a86d (Fixing Request Authentication)
=======

>>>>>>> b3d4630 (Fixed Question Bank)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
<<<<<<< HEAD

<<<<<<< HEAD
=======
>>>>>>> 62669bb (Fixed Deployment missing template sign up)
STATIC_URL = "static/"
STATICFILES_DIRS = ["mentoris/static"]
=======
STATIC_URL = 'static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    'mentoris/static'
]
>>>>>>> ac1cc48 (Configured for elastic beanstalk)


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
=======
# Email Notifications - AWS SES
EMAIL_BACKEND = "django_ses.SESBackend"
<<<<<<< HEAD
>>>>>>> 0b5462f (Implemented Request Translation Email Notification)
=======
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

>>>>>>> b473aa5 (added tables)
=======
=======
# Email Notifications
EMAIL_BACKEND = ""
EMAIL_HOST = ""
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
>>>>>>> e5984d8 (Implement Email Verification & Password Reset)

# Allows Iframes to display from pages hosted by this server
<<<<<<< HEAD
X_FRAME_OPTIONS = 'SAMEORIGIN'
>>>>>>> f354f38 (edit quiz page, added header and footer html files, and colors css file)
=======
X_FRAME_OPTIONS = "SAMEORIGIN"
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 52968c0 (Implemented User Directory and Promotion Page)
=======

AUTH_USER_MODEL = "mentapp.User"
<<<<<<< HEAD
>>>>>>> 489da96 (Changed admin page to use email plus implemented custom user model in app)
=======
=======

AUTH_USER_MODEL = "mentapp.User"
>>>>>>> 1d1ddb5 (edit question functionality)

AUTHENTICATION_BACKENDS = [
    "mentoris.emailauth.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
<<<<<<< HEAD
]
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
=======
]
>>>>>>> 1d1ddb5 (edit question functionality)
