import os
import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from botocore.exceptions import ClientError

from app.models.emails.errors import FailedToSendEmail

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
# SENDER = "Sender Name <sender@example.com>"
SENDER = os.environ.get("SES_VERIFIED_SENDER")


class Email(object):
    def __init__(self, recipients: list, subject: str, attachments=list()):
        self.recipients = recipients
        self.subject = subject
        self.attachments = attachments
        self._text = None
        self._html = None

    def text(self, text):
        self._text = text

    def html(self, html):
        self._html = html

    def create_multipart_message(self) -> MIMEMultipart:
        """
        Creates a MIME multipart message object.
        Uses only the Python `email` standard library.
        Emails, both sender and recipients, can be just the email string or have the format 'The Name <the_email@host.com>'.
        :return: A `MIMEMultipart` to be used to send_email the email.
        """

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = self.subject
        msg['From'] = SENDER
        msg['To'] = ', '.join(self.recipients)

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Record the MIME types of both parts - text/plain and text/html.
        # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is preferred.

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.
        # Add the text and HTML parts to the child container.
        if self._text:
            textpart = MIMEText(self._text.encode('utf-8'), 'plain', 'utf-8')
            msg_body.attach(textpart)
        if self._html:
            htmlpart = MIMEText(self._html.encode('utf-8'), 'html', 'utf-8')
            msg_body.attach(htmlpart)

        # Add attachments
        for attachment in self.attachments:
            with open(attachment, 'rb') as f:
                # Define the attachment part and encode it using MIMEApplication.
                part = MIMEApplication(f.read())
                # Add a header to tell the email client to treat this part as an attachment,
                # and to give the attachment a name.
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                # Add the attachment to the parent container.
                msg.attach(part)

        # Attach the multipart/alternative child container to the multipart/mixed parent container.
        msg.attach(msg_body)
        return msg

    def send_email(self):
        msg = self.create_multipart_message()
        ses_client = boto3.client('ses', region_name='us-east-1',
                                  aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        try:
            # Provide the contents of the email.
            return ses_client.send_raw_email(
                Source=SENDER,
                Destinations=self.recipients,
                RawMessage={'Data': msg.as_string()}
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            raise FailedToSendEmail(e.response['Error']['Message'])
