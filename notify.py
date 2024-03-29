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

def pushbullet_send(access_token, device_iden, title, diffs):
    for diff in diffs:
        url = 'https://api.pushbullet.com/v2/pushes'
        payload = {'title': title, 'body': str(diff), 'url': diff.url, 'type': 'note',
                'device_iden': device_iden}
        headers = {'Access-Token': access_token}
        try:
            req = requests.post(url, data=payload, headers=headers)
            print("PushBullet send: {}".format(req.status_code))
        except Exception as e:
            print(e)
            traceback.print_exc()

def notify(diffs):
    if not len(diffs):
        return
    print(diffs)
    with open('config.yml', 'r') as c:
        config = yaml.safe_load(c)
    title = config.get('message_title', "您检测的网页有动静啦")

    if config.get('server_chan', {}).get('SCKEY', None):
        server_chan_send(config['server_chan']['SCKEY'], title, diffs)

    if os.environ.get('PUSHBULLET_ACCESS_TOKEN') and os.environ.get('PUSHBULLET_DEVICE_IDEN'):
        pushbullet_send(
                os.environ.get('PUSHBULLET_ACCESS_TOKEN'),
                os.environ.get('PUSHBULLET_DEVICE_IDEN'),
                title,
                diffs)
    elif config.get('pushbullet', {}).get('access_token') and config['pushbullet'].get('device_iden'):
        pushbullet_send(
                config['pushbullet']['access_token'],
                config['pushbullet']['device_iden'],
                title,
                diffs)

    if os.environ.get('IFTTT_EVENT') and os.environ.get('IFTTT_KEY'):
        ifttt_send(os.environ.get('IFTTT_EVENT'), os.environ.get('IFTTT_KEY'), title, diffs)
    elif config.get('ifttt', {}).get('key') and config['ifttt'].get('event'):
        ifttt_send(config['ifttt']['event'], config['ifttt']['key'], title, diffs)

    if os.environ.get('SENDGRID_API_KEY') and os.environ.get('SENDGRID_TO'):
        sendgrid_send(os.environ.get('SENDGRID_API_KEY'), os.environ.get('SENDGRID_TO'), title, diffs)
    elif config.get('sendgrid', {}).get('API_KEY') and config.get('sendgrid', {}).get('to'):
        sendgrid_send(config['sendgrid']['API_KEY'], config['sendgrid']['to'], title, diffs)
