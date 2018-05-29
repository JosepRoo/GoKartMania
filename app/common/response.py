class Response(object):
    def __init__(self, success=False, message=None):
        self.success = success
        self.message = message

    def json(self):
        return {'success': self.success,
                'message': self.message
                }
