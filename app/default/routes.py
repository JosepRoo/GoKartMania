from . import default, qrs, documentation


@default.route('/')
def home():
    return default.send_static_file('index.html')


@qrs.route('/<string:id>', methods=['GET'])
def qrs_function(id):
    return qrs.send_static_file(id)


@documentation.route('/apidocs')
def docs():
    return documentation.send_static_file('index.html')
