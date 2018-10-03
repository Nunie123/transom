import sys
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utilities.helpers import get_single_dict_from_json, get_full_path


COMMASPACE = ', '


def get_email_credentials(email_address):
    email_credentials_path = get_full_path(filename='connections.json', subfolder='settings')
    email_credentials_dict = get_single_dict_from_json(email_credentials_path, 'email_address', email_address)
    return email_credentials_dict


class Mailer:
    def __init__(self, sender_address, recipients_list, cc_recipients_list=None, subject='', body='', attachments_list=None):
        self.sender_address = sender_address
        self.recipients_list = recipients_list
        self.subject = subject 
        self.body = body
        email_dict = get_email_credentials(self.sender_address)
        self.username = email_dict.get('email_address')
        self.password = email_dict.get('password')
        self.host = email_dict.get('host')
        self.cc_recipients_list = recipients_list if recipients_list else []
        self.attachments_list = attachments_list if attachments_list else []

    def send_email(self):
        # Create the enclosing (outer) message
        outer = MIMEMultipart('alternative')
        outer['Subject'] = self.subject
        outer['From'] = self.sender_address
        outer['To'] = COMMASPACE.join(self.recipients_list)
        outer['CC'] = COMMASPACE.join(self.cc_recipients_list)

        msg = MIMEBase('application', "octet-stream")

        # Add the text of the email
        email_body = MIMEText(self.body, 'plain')
        outer.attach(email_body)

        # Add the attachments
        for file in self.attachments_list:
            try:
                with open(file, 'rb') as fp:
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition',
                                'attachment',
                                filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to add the attachment to the email")
                raise

        composed = outer.as_string()

            all_recipients = set(self.recipients_list + self.cc_recipients_list)
            all_recipients = list(filter(None, all_recipients))

        try:
            with smtplib.SMTP(host=self.host, port='587') as s:
                s.ehlo()
                s.starttls()
                s.login(self.username, self.password)
                s.sendmail(self.username,
                           all_recipients,
                           composed)
                s.close()
        except smtplib.SMTPConnectError as err:
            print("Unable to connect to the SMTP server to send email: {}".format(err))
            raise
        except:
            print("Unable to send email: {}".format(sys.exc_info()[0]))
            raise

if __name__ == '__main__':
    pass
