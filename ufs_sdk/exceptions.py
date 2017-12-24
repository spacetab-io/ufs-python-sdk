

class UfsAPIError(Exception):
    __slots__ = ['code', 'message', 'message_params']

    def __init__(self, method, error_data, request_data):
        super(UfsAPIError, self).__init__()
        self.method = method
        self.error_data = error_data
        self.request_data = request_data

    def __str__(self):
        msg = 'Method: %s\n' % self.method
        for item in self.error_data:
            msg += '    %s: %s\n' % (item.tag, item.text)
        return msg
