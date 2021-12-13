# This function is not intended to be invoked directly. Instead it will be triggered by an orchestrator function.

import datetime
import requests
import json

from urllib import parse
import azure.functions as func

# Calculate timestamp for this time yesterday
t = datetime.datetime.now() - datetime.timedelta(hours=3)

def main(name):
    tenantId = name['tenantId']
    token = name['token']
    header = {'Authorization' : 'Bearer ' + token}
    host = 'https://manage.office.com/api/v1.0/' + tenantId + '/ServiceComms/Messages'
    params = {"filter": "StartTime ge " + t.strftime('%Y-%m-%dT%H:%M:%SZ')}
    queryStr = parse.urlencode(params)
    url = host + '?$' + queryStr
    response = requests.get(url, headers=header)
    jsonResponse = json.loads(response.text)
    messages = {'tenantId' : tenantId, 'messages' : jsonResponse}
    return(messages)





