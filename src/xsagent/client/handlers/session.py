from contextlib import contextmanager
import os

import XenAPI


@contextmanager
def connection():
    s = XenAPI.Session("http://localhost")
    user = os.getenv('XS_USER', 'root')
    password = os.getenv('XS_PASSWORD', 'xenroot')
    s.login_with_password(user, password)
    yield s
    s.close()
