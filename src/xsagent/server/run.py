import os

from xsagent.server.mq.connect import connect_mq


QUEUE_CONNECT = 'connect'
QUEUE_CMD_RESULT = 'command_result'


def on_connect(channel, method, properties, body):
    pass


def on_cmd_result(channel, method, properties, body):
    pass


def on_channel_open(channel):
    channel.queue_declare(QUEUE_CONNECT)
    channel.queue_declare(QUEUE_CMD_RESULT)
    channel.basic_consume(QUEUE_CONNECT, on_connect, auto_ack=True, consumer_tag='XS-AGENT-SERVER-CONNET')
    channel.basic_consume(QUEUE_CMD_RESULT, on_cmd_result, auto_ack=True, consumer_tag='XS-AGENT-SERVER-COMMAND')
    # FIXME: setup command receiver thread


def main():
    mq_user = os.getenv('RABBITMQ_DEFAULT_USER')
    mq_password = os.getenv('RABBITMQ_DEFAULT_PASS')
    host = 'xs-mq'
    port = 5672
    connect_mq(host, port, mq_user, mq_password, on_channel_open)

if __name__ == '__main__':
    main()
