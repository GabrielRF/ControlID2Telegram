import datetime
import flask
import json
import requests
import telebot
from flask import request

alerts = os.getenv('ALERTS', '1,2,3,4,5,6,7,8,9,10,11,12,13')
bot_token = os.getenv('bot_token')
controlid_ip = os.getenv('controlid_ip')
dest = os.getenv('dest')
password = os.getenv('controlid_password')
webhook_host = os.getenv('webhook_host', '0.0.0.0'
webhook_port = os.getenv('webhook_port', 5432)

app = flask.Flask(__name__)
bot = telebot.TeleBot(bot_token)

def login(controlid_ip, password):
    url = 'http://' + controlid_ip + '/login.fcgi'
    payload = '{\n\t\n\t\"login\":\"admin\",\n\t\"password\":\"'+password+'\"\n\t\n}'
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    session = json.loads(response.text)['session']
    return session

def get_username(controlid_ip, session, userid):
    url = 'http://' + controlid_ip + '/load_objects.fcgi?session=' + session
    payload = ("{\n\t\"object\":\"users\"," +
           "\n\t\n\t\"where\":{" +
           "\n\t\t\"users\":{" +
           "\n\t\t\t\"id\":" + userid +
           "\n\t\t}\n\t}\n}")
    headers = {
        'content-type': 'application/json'
    }

    response = requests.request('POST', url, data=payload, headers=headers)
    response = json.loads(response.text)
    return str(response['users'][0]['name'])

def sendmsg(bot, dest, userid, username, event):
    for i in dest.split(','):
        message = ('{} <b>{}</b> ({})').format(event, username, str(userid))
        bot.send_message(i, message, parse_mode='HTML')

def get_event(eventnum):
    cases = {
        1: 'Equipamento inválido',
        2: 'Parâmetros de regra de identificação inválidos',
        3: str(u'\U000026D4') + 'Não identificado',
        4: 'Identificação pendente',
        5: 'Timeout na identificação',
        6: str(u'\U000026D4'), # 'Acesso negado',
        7: str(u'\U00002705'), # 'Acesso autorizado',
        8: 'Acesso pendente',
        9: 'Usuário não é administrador',
        10: 'Acesso não identificado',
        11: str('\U0001F518') + 'Acesso através de botoeira',
        12: str('\U0001F310') + 'Acesso através de interface web',
        13: 'Desistência de entrada',
    }
    return cases.get(int(eventnum))

@app.route('/api/notification/dao', methods=['POST'])
def index():
    jsonData = request.get_json()
    # deviceid = jsonData['object_changes'][0]['values']['device_id']
    # print(deviceid)
    userid = jsonData['object_changes'][0]['values']['user_id']
    eventnum = jsonData['object_changes'][0]['values']['event']

    if eventnum not in alerts:
        return('')
    session = login(controlid_ip, password)
    try:
        username = get_username(controlid_ip, session, userid)
    except:
        username = ''
    event = get_event(eventnum)
    sendmsg(bot, dest, userid, username, event)
    return('')

if __name__ == '__main__':
    # app.debug = True
    app.run(host=webhook_host, port=webhook_port)

