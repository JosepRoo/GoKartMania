from . import default, qrs


@default.route('/')
def home():
    return default.send_static_file('index.html')


@qrs.route('/<string:id>', methods=['GET'])
def qrs_function(id):
    return qrs.send_static_file(id)