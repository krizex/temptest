from .result import Result
from .session import connection
from xsagent import log


def dispatch(js):
    op = js['operation']
    if op == 'start':
        resp = start(js['vm_uuid'])
    elif op == 'shutdown':
        resp = shutdown(js['vm_uuid'])
    elif op == 'params':
        resp = params(js['vm_uuid'])
    else:
        return Result(1, error_message='Not Implemented')

    return resp

def start(vm_uuid):
    log.info('Start VM %s', vm_uuid)
    try:
        with connection() as s:
            vm = s.xenapi.VM.get_by_uuid(vm_uuid)
            state = s.xenapi.VM.get_power_state(vm)
            if state != 'Running':
                s.xenapi.VM.start(vm, False, False)
    except Exception as e:
        return Result(101, error_message=str(e))
    return Result(0)


def shutdown(vm_uuid):
    log.info('Stop VM %s', vm_uuid)
    try:
        with connection() as s:
            vm = s.xenapi.VM.get_by_uuid(vm_uuid)
            state = s.xenapi.VM.get_power_state(vm)
            if state != 'Halted':
                s.xenapi.VM.shutdown(vm)
    except Exception as e:
        return Result(101, error_message=str(e))
    return Result(0)


def params(vm_uuid):
    log.info('Params of VM')
    with connection() as s:
        vm = s.xenapi.VM.get_by_uuid(vm_uuid)
        name_label = s.xenapi.VM.get_name_label(vm)
        description = s.xenapi.VM.get_name_description(vm)
        power_state = s.xenapi.VM.get_power_state(vm)
        metrics = s.xenapi.VM.get_guest_metrics(vm)
        metrics_record = s.xenapi.VM_guest_metrics.get_record(metrics)

        # make it serializble
        metrics_record['last_updated'] = str(metrics_record['last_updated'])

        result = {
            'UUID': vm_uuid,
            'name_label': name_label,
            'description': description,
            'power_state': power_state,
            'metrics': metrics_record,
        }

    return Result(0, result)
