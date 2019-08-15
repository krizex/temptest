import os
import json

from xsagent.mq.connect import connect_mq
from .info import generate_xs_info
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
    xs_info = generate_xs_info()
    channel.basic_publish(exchange='', routing_key=QUEUE_CONNECT, body=json.dumps(xs_info))
    return xs_info['routing-key']


def create_command_receiver_queue(channel, routing_key):
    def on_queue_declare(frame):
        queue_name = frame.method.queue
        log.info('QUEUE %s declared and bind to %s', queue_name, EXCHANGE_CMD)
        channel.queue_bind(queue_name, EXCHANGE_CMD, routing_key=routing_key)
        channel.basic_consume(queue_name, on_cmd, auto_ack=True)

    def on_exchange_declare(frame):
        channel.queue_declare('', auto_delete=True, callback=on_queue_declare)

    channel.exchange_declare(EXCHANGE_CMD, callback=on_exchange_declare)


def on_channel_open(channel):
    channel.queue_declare(QUEUE_CONNECT)
    channel.queue_declare(QUEUE_CMD_RESULT)
    routing_key = register_client(channel)
    create_command_receiver_queue(channel, routing_key)


def main():
    mq_user = os.getenv('RABBITMQ_DEFAULT_USER')
    mq_password = os.getenv('RABBITMQ_DEFAULT_PASS')
    host = '127.0.0.1'
    port = 8003
    connect_mq(host, port, mq_user, mq_password, on_channel_open)

if __name__ == '__main__':
    main()
