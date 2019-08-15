from aiohttp import web
import json

from xsagent.queuename import EXCHANGE_CMD
from .messages import wait_for_response
from xsagent import log
from xsagent.server.agents import list_agents, agent_exists



def msgid_generator():
    n = 1
    while True:
        yield n
        n += 1

__msgid_gen = msgid_generator()

async def request_agent(channel, routing_key, cmd):
    if not agent_exists(routing_key):
        return {
            'error_code': 201,
            'error_message': 'Server %s does not exist or disconnected' % routing_key
        }
    # generate message id
    msgid = next(__msgid_gen)
    cmd['msgid'] = msgid
    channel.basic_publish(exchange=EXCHANGE_CMD, routing_key=routing_key, body=json.dumps(cmd))
    resp = await wait_for_response(msgid)
    return resp


async def servers(channel, req):
    pools = {}
    agents = list_agents()
    for agent in agents:
        cmd = {
            'type': 'server',
            'operation': 'pool_of',
        }
        resp = await request_agent(channel, agent.routing_key, cmd)
        if resp['error_code'] != 0:
            return web.json_response({'error_code': 401, 'error_message': 'Unable to get pool of %s' % agent})
        pool_uuid = resp['result']
        if pool_uuid not in pools:
            pools[pool_uuid] = []
        pools[pool_uuid].append(agent.__dict__)

    js = {
        'error_code': 0,
        'result': pools
    }
    return web.json_response(js)


# get
# server=xxx
async def server(channel, req):
    routing_key = req.query.get('server')
    cmd = {
        'type': 'server',
        'operation': 'params',
    }
    resp = await request_agent(channel, routing_key, cmd)
    return web.json_response(resp)


# get
# server=xxx&vm=yyy
async def vm(channel, req):
    routing_key = req.query.get('server')
    vm_uuid = req.quer.get('vm')
    cmd = {
        'type': 'vm',
        'operation': 'params',
        'vm_uuid': vm_uuid,
    }

    resp = await request_agent(channel, routing_key, cmd)
    return web.json_response(resp)


# get
# server=routing_key&state=running|halted|None
async def vms_of_server(channel, req):
    agent = req.query.get('server')
    state = req.query.get('state', None)

    log.info('Request CMD list_vms for %s', agent)
    cmd = {
        'type': 'server',
        'operation': 'list_vms',
        'state': state,
    }
    resp = await request_agent(channel, agent, cmd)
    return web.json_response(resp)



# post
# {server:routing_key, vm: vm_uuid}
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


# post
# {server:routing_key, vm: vm_uuid}
async def shutdown_vm(channel, req):
    js = await req.json()
    routing_key = js['server']
    vm_uuid = js['vm']
    cmd = {
        'type': 'vm',
        'operation': 'stop',
        'vm_uuid': vm_uuid,
    }

    resp = await request_agent(channel, routing_key, cmd)
    return web.json_response(resp)
