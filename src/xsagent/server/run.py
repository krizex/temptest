import os
import json

from xsagent.mq.connect import connect_mq
from xsagent import log
from xsagent.queuename import QUEUE_CMD_RESULT, QUEUE_CONNECT
from .agents import add_agent, Agent
from .cmd.messages import set_response
from .cmd.server import CommandServer


def on_connect(channel, method, properties, body):
    log.info('Receive connection from client on XS')
    xs_info = json.loads(body)
    add_agent(xs_info['routing-key'], Agent(xs_info['name'], xs_info['routing-key']))


def on_cmd_result(channel, method, properties, body):
    js = json.loads(body)
    if 'msgid' not in js:
        raise RuntimeError('Incorrect CMD result. Reesult = {}'.format(js))
    msgid = js['msgid']
    log.info('Receive command result from client, msgid = %d', msgid)
    set_response(msgid, js)


def on_channel_open(channel):
    channel.queue_declare(QUEUE_CONNECT)
    channel.queue_declare(QUEUE_CMD_RESULT)
    channel.basic_consume(QUEUE_CONNECT, on_connect, auto_ack=True, consumer_tag='XS-AGENT-SERVER-CONNET')
    channel.basic_consume(QUEUE_CMD_RESULT, on_cmd_result, auto_ack=True, consumer_tag='XS-AGENT-SERVER-COMMAND')
    CommandServer(channel).start()


def main():
    mq_user = os.getenv('RABBITMQ_DEFAULT_USER')
    mq_password = os.getenv('RABBITMQ_DEFAULT_PASS')
    host = 'xs-mq'
    port = 5672
    connect_mq(host, port, mq_user, mq_password, on_channel_open)

if __name__ == '__main__':
    main()
