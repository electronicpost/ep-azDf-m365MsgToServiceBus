# This function is not intended to be invoked directly. Instead it will be triggered by an orchestrator function.

import logging
import json
import os

import azure.functions as func

from urllib import parse
from azure.servicebus import ServiceBusMessage, ServiceBusClient

logging.basicConfig(format='%(asctime)s : %(message)s')

BUS_CONNECTION_STR = os.getenv('busConnStr')
BUS_TOPIC_NAME = 'm365MessageCentre'
MESSAGE_SRC = 'm365MsgToBus'

servicebus_client = ServiceBusClient.from_connection_string(conn_str=BUS_CONNECTION_STR, logging_enable=True)
sender = servicebus_client.get_topic_sender(topic_name=BUS_TOPIC_NAME)


def send(busMessage):
    sender.send_messages(busMessage)

def main(name):
    msgCount = 0
    tenantCount = 0

    # Iterate through full payload, list of dictionaries (per tenant)
    for i, tenant in enumerate(name):
        tenantCount = tenantCount + 1
        tenantId = tenant['tenantId']

        # Iterate through the nested dictionary (value) per tenant containing M365 message.
        for j, msg in enumerate(tenant['messages']['value']):
            msgDict = {'messageBody' : msg}
            msgDict.update({'tenantId': tenantId})
            message = ServiceBusMessage(
                json.dumps(msgDict),
                application_properties={
                    'tenantId': tenantId,
                    'workload': msg['Workload'],
                    'classification': msg['Classification'],
                    'messageType': msg['MessageType'],
                    'messageSrc': MESSAGE_SRC}
                    )
            msgCount = msgCount + 1
            send(message)

    return(f'{msgCount} messages submitted to Service Bus for {tenantCount} tenants.')

 

   

 
