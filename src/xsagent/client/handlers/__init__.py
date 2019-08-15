from . import vm
from . import server
from .result import Result
from xsagent import log


def dispatch_cmd(js):
    try:
        tp = js['type']
        operation = js['operation']
        log.info('CMD type=%s, operation=%s', tp, operation)
        if tp == 'vm':
            return vm.dispatch(js)
        elif tp == 'server':
            return server.dispatch(js)
        else:
            return Result(1, error_message='Not Implemented')
    except Exception as e:
        log.exception('Unable to dispatch cmd: {}'.format(js))
        return Result(999, error_message=str(e))
