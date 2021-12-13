# This function is not intended to be invoked directly. Instead it will be triggered by an orchestrator function.

import json

import azure.functions as func

with open('m365MsgToBus-getTenants/tenants.json') as configFile:
    tenants = json.load(configFile)

def main(name):
    tenantList = []
    for i, tenant in enumerate(tenants['live']):
        reqData = json.dumps(tenant)
        tenantList.append(reqData)
    return tenantList




