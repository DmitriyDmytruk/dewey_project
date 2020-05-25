import os

import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To


def sengrid_send_mail(
    email: str, subject: str, content: str, content_type: str
) -> None:
    """
    Send mail through sendgrid
    :param email:str
    :param subject:str
    :param content:str
    :param content_type:str
    :return:None
    """
    sendgrid_client = sendgrid.SendGridAPIClient(
        api_key=os.environ.get("SENGRID_API_KEY")
    )
    from_email = Email(os.environ.get("SENGRID_EMAIL"))
    to_email = To(email)
    content = Content(content_type, content)
    mail = Mail(from_email, to_email, subject, content)
    sendgrid_client.client.mail.send.post(request_body=mail.get())
