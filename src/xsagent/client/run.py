import os
import json
import signal
import functools
import sys
import time

from xsagent.mq.connect import connect_mq
from .info import xs_info
from xsagent.queuename import EXCHANGE_CMD, QUEUE_CMD_RESULT, QUEUE_CONNECT
from xsagent import log
from .handlers import dispatch_cmd


def on_cmd(channel, method, properties, body):
    log.info('Receive command from server')
    js = json.loads(body)
    result = dispatch_cmd(js)
    result.msgid = js['msgid']
    channel.basic_publish(exchange='', routing_key=QUEUE_CMD_RESULT, body=json.dumps(result.__dict__))


def register_client(channel):
    info = xs_info.copy()
    info['type'] = 'join'
    log.info('Registering the client, name=%s, routing-key=%s', info['name'], info['routing-key'])
    channel.basic_publish(exchange='', routing_key=QUEUE_CONNECT, body=json.dumps(info))


def deregister_client(channel):
    info = xs_info.copy()
    info['type'] = 'leave'
    log.info('Deregistering the client, name=%s, routing-key=%s', info['name'], info['routing-key'])
    channel.basic_publish(exchange='', routing_key=QUEUE_CONNECT, body=json.dumps(info))


def create_command_receiver_queue(channel, routing_key):
    def on_queue_declare(frame):
        queue_name = frame.method.queue
        log.info('QUEUE %s declared and bind to %s', queue_name, EXCHANGE_CMD)
        channel.queue_bind(queue_name, EXCHANGE_CMD, routing_key=routing_key)
        channel.basic_consume(queue_name, on_cmd, auto_ack=True)

    def on_exchange_declare(frame):
        channel.queue_declare('', auto_delete=True, callback=on_queue_declare)

    channel.exchange_declare(EXCHANGE_CMD, callback=on_exchange_declare)


def set_signal_handler(handle):
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
        signal.signal(sig, handle)


def on_channel_open(channel):
    channel.queue_declare(QUEUE_CONNECT)
    channel.queue_declare(QUEUE_CMD_RESULT)
    register_client(channel)
    create_command_receiver_queue(channel, xs_info['routing-key'])
    def sig_handler(signum, frame):
        deregister_client(channel)
        set_signal_handler(signal.SIG_DFL)
        raise RuntimeError('Closing the client')

    set_signal_handler(sig_handler)


def main(host, port, user, password):
    connect_mq(host, port, user, password, on_channel_open)

if __name__ == '__main__':
    host = os.getenv('SERVER_IP', '10.157.11.32')
    port = os.getenv('SERVER_PORT', '1080')
    port = int(port)
    user = 'mq_user'
    password = 'mq_password'
    main(host, port, user, password)
