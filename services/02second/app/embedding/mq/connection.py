# # -*- coding: utf-8 -*
# import os
#
# import pika
#
#
# def getConnectionParam():
#     host = os.getenv("rabbitmq.host")
#     virtualHost = os.getenv("rabbitmq.virtual", "ai-agent")
#     username = os.getenv("rabbitmq.username")
#     password = os.getenv("rabbitmq.password")
#     credentials = pika.PlainCredentials(username, password, erase_on_connect=True)
#     return pika.ConnectionParameters(host, 5672, virtualHost, credentials)
