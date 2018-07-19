class Response(object):
    def __init__(self, success=False, message=None):
        self.success = success
        self.message = message

    def json(self):
        return {'success': self.success,
                'message': self.message
                }

    @classmethod
    def generic_response(cls, e):
        return cls(message=f"Contacta a tu administrador, algo salió mal info: {str(e.__repr__())}").json()
