import os

class EmailConfig:
    SENDER_EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("SECRET")
    PORT = 587
    SMPT_SERVER = "smtp.gmail.com"

class OauthConfig:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")


class Config:
    SQLALCHEMY_DATABASE_URI = None # SQLAlchemy configuration setting
    SECURE_COOKIES = None # Cookies manually created by us configuration setting
    SESSION_COOKIE_SECURE = None # Flask session cookie configuration setting
    REMEMBER_COOKIE_SECURE = None # Flask-Login remember cookie configuration setting
    SESSION_COOKIE_HTTPONLY = None # Flask session cookie configuration setting
    REMEMBER_COOKIE_HTTPONLY = None # Flask-Login remember cookie configuration setting
    SESSION_COOKIE_SAMESITE = None # Flask session cookie configuration setting
    WTF_CSRF_TIME_LIMIT = None # Flask-WTF csrf cookie configuration setting
    OAUTHLIB_INSECURE_TRANSPORT = None #OAUTHLib https configuration setting
    email = EmailConfig()
    oauth = OauthConfig()

class DevelopmentConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
        self.SECURE_COOKIES = False
        self.SESSION_COOKIE_SECURE = False 
        self.REMEMBER_COOKIE_SECURE = False
        self.SESSION_COOKIE_HTTPONLY = True
        self.REMEMBER_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = "None" # Quotes intentional
        self.WTF_CSRF_TIME_LIMIT = None # When set to None, CSRF token is valid for the life of the session
        # self.SQLALCHEMY_ECHO = True # UNCOMMENT TO HAVE SQL OUTPUT TO CONSOLE
        # self.OAUTHLIB_INSECURE_TRANSPORT = 1
 
class ProductionConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_PROD")
        self.SECURE_COOKIES = True
        self.SESSION_COOKIE_SECURE = True 
        self.REMEMBER_COOKIE_SECURE = True
        self.SESSION_COOKIE_HTTPONLY = True
        self.REMEMBER_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = "None" # Quotes intentional
        self.WTF_CSRF_TIME_LIMIT = None # When set to None, CSRF token is valid for the life of the session
        # self.OAUTHLIB_INSECURE_TRANSPORT = 1

def getConfig():
    return DevelopmentConfig() if os.getenv("MODE") == "development" else ProductionConfig()
