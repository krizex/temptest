from threading import Thread
from aiohttp import web
import asyncio
from functools import partial

from xsagent import log
from xsagent.server.cmd import routers


class CommandServer(Thread):
    def __init__(self, channel):
        super(CommandServer, self).__init__()
        self.channel = channel

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = loop.create_server(self.aiohttp_server(), host='0.0.0.0', port='8000')
        log.info('Starting aioHTTPServer')
        loop.run_until_complete(server)
        loop.run_forever()

    def aiohttp_server(self):
        app = web.Application(debug=True)
        app.add_routes([
            web.get('/servers', partial(routers.servers, self.channel)),
            web.get('/server', partial(routers.server, self.channel)),
            web.get('/vms', partial(routers.vms_of_server, self.channel)),
            web.get('/vm', partial(routers.vm, self.channel)),
            web.post('/vm/start', partial(routers.start_vm, self.channel)),
            web.post('/vm/shutdown', partial(routers.shutdown_vm, self.channel)),
        ])
        return app.make_handler()
