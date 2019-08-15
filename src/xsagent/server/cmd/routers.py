from aiohttp import web
import json

from xsagent.queuename import EXCHANGE_CMD
from .messages import wait_for_response
from xsagent import log
from xsagent.server.agents import list_agents


def msgid_generator():
    n = 1
    while True:
        yield n
        n += 1

__msgid_gen = msgid_generator()

async def request_agent(channel, routing_key, cmd):
    # generate message id
    msgid = next(__msgid_gen)
    cmd['msgid'] = msgid
    channel.basic_publish(exchange=EXCHANGE_CMD, routing_key=routing_key, body=json.dumps(cmd))
    resp = await wait_for_response(msgid)
    return resp


async def hello(channel, req):
    log.info('CMD: hello')
    return web.json_response({'result': 0})


async def servers(req):
    agents = list_agents()
    agents = [agent.__dict__ for agent in agents]
    js = json.dumps(agents)

    return web.json_response(js)


async def vms_of_server(channel, req):
    server = req.query.get('server', None)
    if server is None:
        agents = list_agents()
        agents = [agent.routing_key for agent in agents]
    else:
        agents = [server]

    result = {
        'error_code' : 0,
        'result' : {},
    }
    for agent in agents:
        log.info('Request CMD list_vms for %s', agent)
        cmd = {
            'type': 'server',
            'operation': 'list_vms',
        }
        resp = await request_agent(channel, agent, cmd)
        if resp['error_code'] != 0:
            return web.json_response({'error_code': 1, 'error_message': 'unable to list VMs of %s' % agent})
        result['result'][agent] = resp['result']

    return web.json_response(result)



async def start_vm(channel, req):
    js = await req.json()
    routing_key = js['server']
    vm_uuid = js['vm']
    cmd = {
        'type': 'vm',
        'operation': 'start',
        'vm_uuid': vm_uuid,
    }

    resp = await request_agent(channel, routing_key, cmd)
    return web.json_response(resp)


