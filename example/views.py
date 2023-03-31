# example/views.py
from datetime import datetime
from agora_token_builder import RtcTokenBuilder
from django.http import HttpResponse
import json

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
    appId='4f5f1bf38e0c440f86d3b1df203195c8'
    appCertificate='9e95450e6f7749b18cb30af425c20f90'
    channelName=req.GET.get('channelName')
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, 1,1,3600 )
    response={"token":token}
    return json.dumps(response)