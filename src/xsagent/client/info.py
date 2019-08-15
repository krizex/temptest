import os
import commands
import uuid

def generate_routing_key():
    return str(uuid.uuid1())


def host_uuid():
    ret = commands.getstatusoutput("cat /etc/xensource-inventory | grep INSTALLATION_UUID | awk -F'=' '{print $2}'")
    return ret[1].replace("'", '')


def __generate_xs_info():
    return {
        'name': os.uname()[1],
        'routing-key': generate_routing_key(),
        'uuid': host_uuid(),
    }

xs_info = __generate_xs_info()
