from functions import *
import json
import requests

url = 'http://localhost:8080/'

c=Car(2,16,get_mac())


payload = json.loads(payload(c))
headers = {'content-type': 'application/json'}
r = requests.post(url, data = json.dumps(payload), headers = headers)





