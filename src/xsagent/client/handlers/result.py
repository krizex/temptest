
class Result:
    def __init__(self, error_code, result=None, error_message=None):
        self.error_code = error_code
        self.result = result
        self.error_message = error_message
        self.msgid = None
