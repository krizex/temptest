from threading import Thread
from aiohttp import web
import asyncio
from functools import partial


async def hello(channel, req):
    return web.Response('hello!')


class CommandServer(Thread):
    def __init__(self, channel):
        super(CommandServer, self).__init__()
        self.channel = channel

    def run(self):
        loop = asyncio.get_event_loop()
        server = loop.create_server(self.aiohttp_server(), host='0.0.0.0', port='8001')
        loop.run_until_complete(server)
        loop.run_forever()

    def aiohttp_server(self):
        app = web.Application(debug=True)
        app.add_routes([
            web.get('/hello', partial(hello, self.channel))
        ])
        return app.make_handler()
