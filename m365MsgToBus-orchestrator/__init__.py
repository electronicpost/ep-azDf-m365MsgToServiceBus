# This function is not intended to be invoked directly. Instead it will be triggered by an HTTP starter function.
# Orchestration currently is not passed any varables, intend to have the message time period passed in future.

# The following is the orchestration sequence:
# 01 getTenants: Obtain list of tenants from config file to retrieve M365 messages for (plan to later move this to separate API)
# 02 getToken (Fan Out): Iterate through each tenant and obtain token for message request.
# 03 reqList (Fan In): Compiled list of tenant id's and tokens.
# 04 getMessages (Fan Out): Iterate through each tenant and retrieve M365 messages.
# 05 msgList (Fan In): Compiled list of tenant id's and messages.
# 06 finalMsgCount: Count of the number of messages collected across the number of tenants

import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    tenants = yield context.call_activity('m365MsgToBus-getTenants')

    # Emtpy list to store the tenant id's and tokens for the individual requests.
    msgRequests = []
    for tenant in tenants:
        msgRequests.append(context.call_activity('m365MsgToBus-getToken', tenant))
    reqList = yield context.task_all(msgRequests)

    # Emtpy list to store the tenant id's along with their M365 messages.
    messages = []
    for req in reqList:
        messages.append(context.call_activity('m365MsgToBus-getMessages', req))
    msgList = yield context.task_all(messages)

    finalMsgCount = yield context.call_activity('m365MsgToBus-sendMessages', msgList)
    return [finalMsgCount]

main = df.Orchestrator.create(orchestrator_function)





