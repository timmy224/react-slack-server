from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ...constants.email import email_settings

def create_text_email_new_user(sender, org_name):
    text_email = f"""
                    Hello!
                    Join {org_name} on React Slack
                    {sender} has invited you to join the React Slack workspace {org_name} 
                    www.reactslack.com
                    """
    return text_email

def create_html_email_new_user(sender, org_name):
    html_email = f"""
                    <html>
                        <body>
                            <p>Hello!</p>
                            <h1>Join {org_name} on React Slack</h1>
                            <p>{sender} has invited you to join the React Slack workspace {org_name}</p>
                            <a href="http://www.reactslack.com">React Slack</a> 
                        </body>
                    </html>
                    """
    return html_email

def create_email_subject_new_user(sender):
    subject = f"{sender}, has invited you to join a react_slack workspace"
    return subject

def create_email(sender, receiver_email, text, html, subject):
    message = MIMEMultipart("alternative")
    message["subject"] = subject
    message["From"] = email_settings.SENDER_EMAIL
    message["To"] = receiver_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    return message
