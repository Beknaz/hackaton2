from .celery import  app

from .helpers import  send_confirmation_email
@app.task
def send_conf_emails(email, code):
    send_confirmation_email(email, code)