import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False


class Local(Config):
    DEBUG = True


class Test(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_TEST")


class Prod(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_PROD")


configs = dict(
    local=Local,
    test=Test,
    # development=Dev,
    # staging=Staging,
    production=Prod,
)

config = configs[os.getenv("FLASK_ENV", "local")]
