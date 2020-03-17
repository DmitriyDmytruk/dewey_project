import sendgrid
import os
from sendgrid.helpers.mail import Email, To, Content, Mail


def sengrid_send_mail(email: str, subject: str, content: str, content_type: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENGRID_API_KEY'))
    from_email = Email(os.environ.get('SENGRID_EMAIL'))
    to_email = To(email)
    content = Content(content_type, content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
