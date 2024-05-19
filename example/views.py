# example/views.py
# from validate_email_address import validate_email
from datetime import datetime
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse, JsonResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(name='',email='',message='',**kvargs):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'gowthamgopi444@gmail.com'  # Your email address
    smtp_password = os.environ.get('SMTP_PASSWORD')  # Your email password

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'gowthamgopi184@gmail.com'
    msg['Subject'] = 'Daily Report'

    body = f'Hello Gowtham,\n\n{message}\n\nRegards,\n{name}\n{email}'

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email
        server = smtplib.SMTP(smtp_server, smtp_port)  # Update with your SMTP server and port
        server.starttls()
        server.login(smtp_user, smtp_password)  # Update with your email and password
        server.send_message(msg)
        print(f"Email sent successfully to {msg['To']}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        # Close the SMTP server
        server.quit()

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
            <a href="./generate?">Generate token</a><br/>
            <a href="./mail">Mail To</a><br/>
            <a href="./keys">Openai key</a><br/>
        </body>
    </html>
    '''
    return HttpResponse(html)


def generate(req):
    appId = os.environ.get('appId')
    appCertificate = os.environ.get('appCertificate')
    channelName = 'channleName'
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, 1, 1, 3600)
    res = {'token': token}
    return JsonResponse(res)


def mailto(req):
    try:
        name=req.GET['name']
        email=req.GET['email']
        content=req.GET['message']
        send_email(name,email,content)
        return HttpResponse(status=400)
    except:
        return HttpResponse(status=400)

def keys(req):
    return JsonResponse({"key":os.environ.get('key')})