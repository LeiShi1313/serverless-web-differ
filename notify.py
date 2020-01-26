import os
import yaml
import requests
import traceback
from collections import namedtuple
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class WebDiff(namedtuple('WebDiff', ['title', 'url', 'original', 'current'])):
    __slots__ = ()

    def __str__(self):
        return "{}: {} -> {}\n{}".format(self.title, self.original, self.current, self.url)

def sendgrid_send(api_key, to, title, diffs):
    message = Mail(
        from_email='web_differ@leishi.io',
        to_emails=to,
        subject=title,
        html_content='<br><br>'.join(map(str, diffs)))
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("Sendgrid send: {}".format(response.status_code))
    except Exception as e:
        print(e)
        traceback.print_exc()

def ifttt_send(event, key, title, diffs):
    for diff in diffs:
        payload = {'value1': title, 'value2': str(diff), 'value3': diff.url}
        url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event, key)
        try:
            req = requests.post(url, data=payload)
            print("IFTTT send: {}".format(req.status_code))
        except Exception as e:
            print(e) 
            traceback.print_exc()

def server_chan_send(sckey, title, diffs):
    for diff in diffs:
        url = 'https://sc.ftqq.com/{}.send?text={}&desp={}'.format(sckey, title, str(diff))
        try:
            req = requests.get(url)
            print("Server Chan send: {}".format(req.status_code))
        except Exception as e:
            print(e) 
            traceback.print_exc()



def notify(diffs):
    if not len(diffs):
        return
    with open('config.yml', 'r') as c:
        config = yaml.safe_load(c)
    title = config.get('message_title', "您检测的网页有动静啦")

    if config.get('server_chan', {}).get('SCKEY', None):
        server_chan_send(config['server_chan']['SCKEY'], title, diffs)

    if os.environ('IFTTT_EVENT') and os.environ('IFTTT_KEY'):
        ifttt_send(os.environ('IFTTT_EVENT'), os.environ('IFTTT_KEY'), title, diffs)
    elif config.get('ifttt', {}).get('key', None) and config['ifttt'].get('event', None):
        ifttt_send(config['ifttt']['event'], config['ifttt']['key'], title, diffs)
    
    if os.environ('SENDGRID_API_KEY') and os.environ('SENDGRID_TO'):
        sendgrid_send(os.environ('SENDGRID_API_KEY'), os.environ('SENDGRID_TO'), title, diffs)
    elif config.get('sendgrid', {}).get('API_KEY', None) and config.get('sendgrid', {}).get('to', None):
        sendgrid_send(config['sendgrid']['API_KEY'], config['sendgrid']['to'], title, diffs)