from dotenv import load_dotenv
from math import inf as infinity
from os import environ

load_dotenv()


ADMIN_EMAIL = environ.get("ADMIN_EMAIL")


# Debugging value for the app
DEBUG = True


CONFIG = {
    "DEBUG": True,
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": "cache-directory",
    'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
    'CACHE_THRESHOLD': infinity,
}



# The variables responsible for displaying the CKEDITOR for the site
CKEDITOR_ENABLE_CSRF = True
CKEDITOR_HEIGHT = 1000
CKEDITOR_PKG_TYPE = "full"


# Database name
DB_HOST = environ["DB_HOST"]
DB_NAME = environ['DB_NAME']
DB_PASSWORD = environ["DB_PASSWORD"]
DB_USERNAME = environ["DB_USERNAME"]

#DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"


# Enirionment for development
FLASK_ENV = 'production'


# Hostname for the site
HOSTNAME = "http://127.0.0.1:5000"


#Mysql root password
MYSQL_ROOT_PASSWORD = environ["MYSQL_ROOT_PASSWORD"]


# Sqlachemy variables
SQLALCHEMY_DATABASE_URI = "sqlite:///jobJournal.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 299


# The secret key
SECRET_KEY = environ.get("SECRET_KEY")


