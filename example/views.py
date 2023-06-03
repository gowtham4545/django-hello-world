# example/views.py
from validate_email_address import validate_email
from datetime import datetime
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.core.mail import send_mail


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)


def generate(req):
    appId = '4f5f1bf38e0c440f86d3b1df203195c8'
    appCertificate = '9e95450e6f7749b18cb30af425c20f90'
    channelName = req.GET.get('channelName')
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, 1, 1, 3600)
    res = {'token': token}
    return JsonResponse(res)


def mailto(req):
    get = req.GET
    frm = get['id']
    name = get['name']
    sub = get['subject']
    bdy = get['body']
    isExists = validate_email(frm, verify=True)
    print(isExists)
    if not isExists:
        return JsonResponse({'status': 402})
    fromaddr = "gowthamgopi444@gmail.com"
    toaddr = "gowthamgopi444@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = frm
    msg['To'] = toaddr
    msg['Subject'] = sub
    body = f'''
        From : {frm}
        Name : {name}

        {bdy}
    '''
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, 'gouanborkddpapcp')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    return JsonResponse({'status': 200})
