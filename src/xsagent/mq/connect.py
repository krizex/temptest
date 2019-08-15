import pika
from xsagent import log


def connect_mq(host, port, user, password, on_channel_open, on_close_callback=None):
    def on_open(connection):
        log.info('MQ connected')
        connection.channel(on_open_callback=on_channel_open)

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, '/', credentials)
    connection = pika.SelectConnection(parameters=parameters, on_open_callback=on_open)
    try:
        connection.ioloop.start()
    except:
        # Gracefully close the connection
        connection.close()
        # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
        connection.ioloop.start()


