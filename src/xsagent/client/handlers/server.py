from .result import Result

from xsagent import log
from .session import connection
from xsagent.client.info import xs_info

def dispatch(js):
    op = js['operation']
    if op == 'list_vms':
        resp = list_vms(js['state'])
    elif op == 'pool_of':
        resp = pool_of_server()
    elif op == 'params':
        resp = params()
    else:
        return Result(1, error_message='Not Implemented')

    return resp


def list_vms(state):
    log.info('list vms')
    vms = []
    with connection() as s:
        all_vms = s.xenapi.VM.get_all()
        for vm in all_vms:
            is_template = s.xenapi.VM.get_is_a_template(vm)
            if not is_template:
                power_state = s.xenapi.VM.get_power_state(vm)
                if state is not None and power_state != state:
                    continue

                host = s.xenapi.VM.get_resident_on(vm)
                if host != 'OpaqueRef:NULL':
                    host_uuid = s.xenapi.host.get_uuid(host)
                    if host_uuid != xs_info['uuid']:
                        continue
                uuid = s.xenapi.VM.get_uuid(vm)
                vms.append(uuid)

    return Result(0, vms)

def pool_of_server():
    log.info('Pool of server')
    vms = []
    with connection() as s:
        pool = s.xenapi.pool.get_all()[0]
        uuid = s.xenapi.pool.get_uuid(pool)

    return Result(0, uuid)


def params():
    log.info('Params of server')
    with connection() as s:
        host_uuid = xs_info['uuid']
        host = s.xenapi.host.get_by_uuid(host_uuid)
        name_label = s.xenapi.host.get_name_label(host)
        description = s.xenapi.host.get_name_description(host)
        metrics = s.xenapi.host.get_metrics(host)
        metrics_record = s.xenapi.host_metrics.get_record(metrics)

        # make it serializble
        metrics_record['last_updated'] = str(metrics_record['last_updated'])


        result = {
            'UUID': host_uuid,
            'name_label': name_label,
            'description': description,
            'metrics': metrics_record,
        }

    return Result(0, result)
