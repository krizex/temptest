import XenAPI
from contextlib import contextmanager


@contextmanager
def connection():
    s = XenAPI.Session("http://localhost")
    s.login_with_password("root", "xenroot")
    yield s
    s.close()
