from .result import Result

def dispatch(js):
    operation = js['operation']
    if operation == 'start':
        resp = start(js['vm_uuid'])
    else:
        return Result(1, error_message='Not Implemented')

    return resp

def start(vm_uuid):
    log.info('Start VM %s', vm_uuid)
    return Result(0)
