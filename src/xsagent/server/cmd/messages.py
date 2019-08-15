import threading
import asyncio


class Message:
    def __init__(self, msgid, loop, event, response):
        self.msgid = msgid,
        self.loop = loop
        self.event = event
        self.response = response


__lock = threading.Lock()
__messages = {}


async def wait_for_response(msgid):
    event = asyncio.Event()
    loop = asyncio.get_running_loop()
    with __lock:
        __messages[msgid] = Message(msgid, loop, event, None)

    await event.wait()
    return get_response(msgid)


def get_response(msgid):
    with __lock:
        msg = __messages.pop(msgid, None)

    if msg is None:
        raise RuntimeError('Message %d does not exist', msgid)

    response = msg.response
    if response is None:
        raise RuntimeError('Response of message %d is None', msgid)

    return response


def set_response(msgid, response):
    with __lock:
        if msgid not in __messages:
            log.error('Cannot find message of id %d', msgid)
            return
        else:
            msg = __messages[msgid]
            msg.response = response
            msg.loop.call_soon_threadsafe(lambda: msg.event.set())

