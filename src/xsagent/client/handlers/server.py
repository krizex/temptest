from .result import Result

from xsagent import log

def dispatch(js):
    operation = js['operation']
    if operation == 'list_vms':
        resp = list_vms()
    else:
        return Result(1, error_message='Not Implemented')

    return resp


def list_vms():
    log.info('list vms')
    vms = [
        '111',
        '222',
        '333'
    ]

    return Result(0, vms)
