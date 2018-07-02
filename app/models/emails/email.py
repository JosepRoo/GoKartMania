import os
import boto.ses
from app.models.emails.errors import FailedToSendEmail

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")


class Email(object):
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
        self._format = 'html'

    def html(self, html):
        """
        Sets the html attribute to the given parameter
        :param html: The HTML code to be set to the email
        :return: None
        """
        self._html = html

    def text(self, text):
        """
        Sets the text attribute to the given parameter
        :param text: The text body that the email will show
        :return: None
        """
        self._text = text

    def send(self, from_addr=None):
        """
        Send the email from a given address, with a certain body, to a given user
        :param from_addr: The address sending the email
        :return: SES connection with the sent email object
        """
        body = self._html

        if isinstance(self.to, str):
            self.to = [self.to]
        if not from_addr:
            from_addr = 'contacto@iualia.com'
        if not self._html and not self._text:
            raise FailedToSendEmail('Debes proporcionar un mensaje de texto o cuerpo HTML válido.')
        if not self._html:
            self._format = 'text'
            body = self._text

        connection = boto.ses.connect_to_region(
            'us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )

        return connection.send_email(
            from_addr,
            self.subject,
            None,
            self.to,
            format=self._format,
            text_body=self._text,
            html_body=self._html
        )
