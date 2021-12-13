# This function is not intended to be invoked directly. Instead it will be triggered by an orchestrator function.

import os
import requests
import json

from urllib import parse
import azure.functions as func

resource = 'https://manage.office.com'

def main(name: str) -> str:
    data = json.loads(name)
    clientSecret = os.getenv(data['secretKey'])
    clientId = data['clientId']
    tenantId = data['tenantId']
    tokenHost = 'https://login.microsoftonline.com/' + tenantId + '/oauth2/token'
    params = {'resource' : resource, 'client_id' : clientId, 'client_secret' : clientSecret, 'grant_type' : 'client_credentials'}
    body = parse.urlencode(params).encode("utf-8")
    response = requests.get(tokenHost, data=body)
    jsonResponse = json.loads(response.text)
    aadToken = jsonResponse["access_token"]
    tenantReq = {'tenantId' : tenantId,'token' : aadToken}
    return(tenantReq)



    