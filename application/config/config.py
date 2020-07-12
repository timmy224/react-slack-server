import os

class Config:
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
 
class ProductionConfig(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_PROD")

def getConfig():
    return DevelopmentConfig() if os.getenv("MODE") == "development" else ProductionConfig()