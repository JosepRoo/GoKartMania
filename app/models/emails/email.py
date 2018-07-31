import os
import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from botocore.exceptions import ClientError

from app.models.emails.errors import FailedToSendEmail

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

"""
This is the email model that will be used to handle the requests of sending emails to the user, the admin, and pilots
"""


class Email(object):
    def __init__(self, to, subject, qr_code):
        self.to = to
        self.subject = subject
        self.qr_code = qr_code
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
            pass
            # self.to = [self.to]
        if not from_addr:
            from_addr = 'contacto@iualia.com'
        if not self._html and not self._text:
            raise FailedToSendEmail('Debes proporcionar un mensaje de texto o cuerpo HTML valido.')
        if not self._html:
            self._format = 'text'
            body = self._text

        connection = boto3.client('ses',
                                  region_name='us-east-1',
                                  aws_access_key_id=AWS_ACCESS_KEY,
                                  aws_secret_access_key=AWS_SECRET_KEY
                                  )

        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = self.subject
        msg['From'] = from_addr
        msg['To'] = self.to

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.
        textpart = MIMEText(self._text.encode("utf-8"), 'plain', "utf-8")
        htmlpart = MIMEText(self._html.encode("utf-8"), 'html', "utf-8")

        # Add the text and HTML parts to the child container.
        msg_body.attach(textpart)
        msg_body.attach(htmlpart)

        # Define the attachment part and encode it using MIMEApplication.
        #att = MIMEApplication(open(self.qr_code, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        #att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.qr_code))

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        #msg.attach(att)

        try:
            # Provide the contents of the email.
            response = connection.send_raw_email(
                Source=from_addr,
                Destinations=[
                    self.to
                ],
                RawMessage={
                    'Data': msg.as_string(),
                }
            )
            return response
        # Display an error if something goes wrong.
        except ClientError as e:
            raise FailedToSendEmail(e.response['Error']['Message'])
