from datetime import datetime
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse, JsonResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_email(name='', email='', message='', subject='Redirected Mail', **kvargs):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'gowthamgopi444@gmail.com'
    smtp_password = os.environ.get('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'gowtham.off.4545@gmail.com'
    msg['Subject'] = subject

    body = f'{message}\n\nRegards,\n{name}\n{email}'

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(msg)
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
        name = req.GET.get('name')
        email = req.GET.get('email')
        content = req.GET.get('message')
        topic = req.GET.get('subject')
        if topic:
            send_email(name, email, content, topic)
        else:
            send_email(name, email, content)
        return JsonResponse({"status": 0})
    except Exception as e:
        return JsonResponse({
            "status":1,
            "error": str(e)
        })


def keys(req):
    return JsonResponse({"key": os.environ.get('key')})
