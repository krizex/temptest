import os
import uuid


def generate_routing_key():
    return str(uuid.uuid1())


def generate_xs_info():
    return {
        'name': 'XenServer xxxx',
        'routing-key': generate_routing_key()
    }
