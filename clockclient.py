import json
import os
import time
import requests
from ws4py.client.threadedclient import WebSocketClient


username = 'LanceBot'
password = '1352040930'
channel_ = 'lounge'
api = 'ws://chat.henrize.kim:6060/'


def get_hitokoto():
    hitokoto_api = 'https://v1.hitokoto.cn/?charset=utf8&encode=json&c=b'
    js = json.loads(requests.get(hitokoto_api).text)
    text = '> %s\n-- %s' % (js['hitokoto'], js['from'])
    return text


class Settings:
    def __init__(self):
        self.save_filename = 'chat.json'
        self.username = username
        self.password = password
        self.channel = channel_


class MyClient(WebSocketClient):
    def opened(self):
        global connected
        settings = Settings()
        channel = settings.channel
        if channel == '':
            channel = channel_
        # print(self.channel)
        if len(settings.password) > 0 and '#' not in settings.username:
            user = "%s#%s" % (settings.username, settings.password)
        else:
            user = settings.username
        req = json.dumps({"cmd": "join", "channel": channel, "nick": user})
        self.send(req)
        connected = True

    def closed(self, code, reason=None):
        global connected
        # print("Closed down:", code, reason)
        connected = False

    def send_text(self, text):
        data = json.dumps({'cmd': 'chat', "text": text})
        print('<-', data)
        self.send(data)

    def received_message(self, resp):
        global var_text
        print('->', resp)
        try:
            resp = json.loads(str(resp))
        except Exception as e:
            print(resp, e)
            return
        data = resp
        print(data)


def main(event=None, context=None):
    ws = MyClient(api)
    ws.connect()
    time.sleep(0.1)
    now = time.asctime().split()[3]
    ws.send_text('大家好我是Lance。美好的一天又开始了~\n\n%s' % (get_hitokoto(), ))
    time.sleep(0.1)
    ws.close()
    time.sleep(0.1)


if __name__ == '__main__':
    main()
