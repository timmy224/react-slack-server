import os

class Config:
    SQLALCHEMY_DATABASE_URI = None # SQLAlchemy configuration setting
    SECURE_COOKIES = None # Cookies manually created by us configuration setting
    SESSION_COOKIE_SECURE = None # Flask session cookie configuration setting
    REMEMBER_COOKIE_SECURE = None # Flask-Login remember cookie configuration setting
    SESSION_COOKIE_HTTPONLY = None # Flask session cookie configuration setting
    REMEMBER_COOKIE_HTTPONLY = None # Flask-Login remember cookie configuration setting
    SESSION_COOKIE_SAMESITE = None # Flask session cookie configuration setting
    WTF_CSRF_TIME_LIMIT = None # Flask-WTF csrf cookie configuration setting

class Email(Config):
    def __init__(self):
        self.SENDER_EMAIL = "react.slack2020@gmail.com"
        self.PASSWORD = os.getenv("SECRET")
        self.PORT = 587
        self.SMPT_SERVER = "smtp.gmail.com"

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

def getConfig():
    return DevelopmentConfig() if os.getenv("MODE") == "development" else ProductionConfig()
