import os

class Config:
    SQLALCHEMY_DATABASE_URI = None # SQLAlchemy configuration setting
    SECURE_COOKIES = None # Cookies manually created by us configuration setting
    SESSION_COOKIE_SECURE = None # Flask-Login session cookie configuration setting
    REMEMBER_COOKIE_SECURE = None # Flask-Login remember cookie configuration setting

class DevelopmentConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
        self.SECURE_COOKIES = False
        self.SESSION_COOKIE_SECURE = False 
        self.REMEMBER_COOKIE_SECURE = False
 
class ProductionConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_PROD")
        self.SECURE_COOKIES = True
        self.SESSION_COOKIE_SECURE = True 
        self.REMEMBER_COOKIE_SECURE = True

def getConfig():
    return DevelopmentConfig() if os.getenv("MODE") == "development" else ProductionConfig()