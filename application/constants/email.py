import os

class EmailSettings:
    SENDER_EMAIL = "react.slack2020@gmail.com"
    PASSWORD = os.getenv("SECRET")
    PORT =  465
    SMPT_SERVER = "smtp.gmail.com"

email_settings = EmailSettings()
