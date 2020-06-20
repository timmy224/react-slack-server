import os

class Config:
    SQLALCHEMY_DATABASE_URI = ""

class DevelopmentConfig(Config):
    def __init__(self):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
 
class ProductionConfig(Config):
    def __init__(self):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_PROD")

def getConfig():
    return DevelopmentConfig() if os.getenv("MODE") == "development" else ProductionConfig()