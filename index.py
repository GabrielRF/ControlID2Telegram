import flask
import json
import os
import requests
import telebot
from flask import request

alerts = os.getenv('ALERTS', '1,2,3,4,5,6,7,8,9,10,11,12,13')
bot_token = os.getenv('BOT_TOKEN')
controlid_ip = os.getenv('CONTROLID_IP')
host_ip = os.getenv('HOST_IP')
dest = os.getenv('MESSAGE_DESTINATION')
cid_webuser = os.getenv('CONTROLID_USER', default='admin')
cid_webpassword = os.getenv('CONTROLID_PASSWORD', default='admin')
webhook_host = os.getenv('WEBHOOK_HOST', '0.0.0.0')
webhook_port = os.getenv('WEBHOOK_PORT', 5432)

app = flask.Flask(__name__)
bot = telebot.TeleBot(bot_token)

def set_monitor():
    url = "http://" + controlid_ip + "/login.fcgi"

    payload_dict = {}
    payload_dict['login'] = str(cid_webuser)
    payload_dict['password'] = str(cid_webpassword)
    payload=json.dumps(payload_dict)

    headers = {
        'content-type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    session = json.loads(response.text)['session']

    url = "http://" + controlid_ip + "/set_configuration.fcgi?session=" + session
    payload_dict = {'monitor': {
                'request_timeout': str(500),
                'hostname': str(host_ip),
                'port': str(webhook_port),
                'path': 'api/notification'
                }
            }
    payload = json.dumps(payload_dict, indent=4)
    print(payload)
    headers = {
        'content-type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(str(response))

def login(controlid_ip, password):
    url = 'http://' + controlid_ip + '/login.fcgi'
    payload_dict = {'login': cid_webuser, 'password': cid_webpassword}
    payload = json.dumps(payload_dict)
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    session = json.loads(response.text)['session']
    return session

def get_username(controlid_ip, session, userid):
    url = 'http://' + controlid_ip + '/load_objects.fcgi?session=' + session
    payload_dict = {
            'object': 'users',
            'where': {
                'users': {
                    'id': int(userid)
                    }
                }
            }
    payload = json.dumps(payload_dict, indent=4)
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
        200: 'Equipamento ligado',
        
    }
    return cases.get(int(eventnum))

@app.route('/api/notification/dao', methods=['POST'])
def index():
    jsonData = request.get_json()
    userid = jsonData['object_changes'][0]['values']['user_id']
    eventnum = jsonData['object_changes'][0]['values']['event']

    if eventnum not in alerts:
        return('')
    session = login(controlid_ip, cid_webpassword)
    try:
        username = get_username(controlid_ip, session, userid)
    except:
        username = ''
    event = get_event(eventnum)
    sendmsg(bot, dest, userid, username, event)
    return('')

@app.route('/api/notification/operation_mode', methods=['POST'])
def op_mode():
    jsonData = request.get_json()
    mode = jsonData['operation_mode']['mode']
    mode_name = jsonData['operation_mode']['mode_name']
    last_offline = jsonData['operation_mode']['last_offline']
    print(str(mode) + '\t' + mode_name + '\t' + str(last_offline))
    if last_offline == 0:
        event = get_event(200)
        sendmsg(bot, dest, '', '', event)
    return('')


@app.route('/api/notification/secbox', methods=['POST'])
def secbox():
    jsonData = request.get_json()
    id = jsonData['secbox']['id']
    open = jsonData['secbox']['open']
    print(str(id) + '\t' + str(open))
    return('')

if __name__ == '__main__':
    # app.debug = True
    set_monitor()
    app.run(host=webhook_host, port=webhook_port)


