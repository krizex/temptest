from xsagent import log


class Agent:
    def __init__(self, name, routing_key):
        self.name = name
        self.routing_key = routing_key

    def __str__(self):
        return f'Agent <name: {self.name}, routing-key: {self.routing_key}>'


def add_agent(routing_key, agent):
    log.info('Add agent %s', agent)
    __agents[routing_key] = agent


def del_agent(routing_key):
    log.info('Add agent %s', routing_key)
    del __agents[routing_key]


def list_agents():
    return list(__agents.values())




__agents = {}
