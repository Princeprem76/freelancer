import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Util:
    @staticmethod
    def send_email(data):
        message = Mail(
            from_email='princepreem1@gmail.com',
            to_emails=data['email'],
            subject=data['subject'],
            html_content=data['email_body'],)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(data['email_body'])
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)