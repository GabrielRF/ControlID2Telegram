import requests
import json

controlid_ip = os.getenv('CONTROLID_IP')
password = os.getenv('CONTROLID_PASSWORD')
dockerhip = os.getenv('HOST_IP')
dockerport = os.getenv('WEBHOOK_PORT')

url = "http://" + controlid_ip + "/login.fcgi"

payload = '{\n\t\n\t\"login\":\"admin\",\n\t\"password\":\"'+password+'\"\n\t\n}'
headers = {
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)
session = json.loads(response.text)['session']

url = "http://" + controlid_ip + "/set_configuration.fcgi?session=" + session
print(url)
payload = ("{\n\t\n\t\"monitor\":" +
           "{\n\t\n\t\"request_timeout\":\"500\"," +
           "\n\t\"hostname\":\"" + dockerhip + "\"," +
           "\n\t\"port\":\"" + dockerport + "\"," +
           "\n\t\"path\":\"api/notification\"\n}\n}")
print(payload)
headers = {
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(str(response))

