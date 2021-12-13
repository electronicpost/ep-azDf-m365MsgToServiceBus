# ep-azDf-m365MsgToServiceBus

Azure Durable Function to get messages from Microsoft 365 Message Centre for multiple tenants and submit those messages to an Azure Service Bus for further processing.

Config Items:
- m365MsgToBus-getTenants/tenants.json, config file for list of tenants, the secret is a reference to be looked up within a Key Vault.

m365MsgToBus-sendMessages
- busConnStr, is a reference to be looked up within a Key Vault for the connection string to your Azure Service Bus Namespace.
- m365MessageCentre, name of the topic to deliver messages to within the service bus. 

This function is not intended to be invoked directly. Instead it will be triggered by an HTTP starter function.
Orchestration currently is not passed any varables, intend to have the message time period passed in future.

The following is the orchestration sequence:
- 01 getTenants: Obtain list of tenants from config file to retrieve M365 messages for (plan to later move this to separate API)
- 02 getToken (Fan Out): Iterate through each tenant and obtain token for message request.
- 03 reqList (Fan In): Compiled list of tenant id's and tokens.
- 04 getMessages (Fan Out): Iterate through each tenant and retrieve M365 messages.
- 05 msgList (Fan In): Compiled list of tenant id's and messages.
- 06 finalMsgCount: Count of the number of messages collected across the number of tenants

