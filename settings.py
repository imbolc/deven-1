DEBUG = False
HOST = 'localhost'
PORT = 5000
MONGO_URI = 'mongodb://localhost/deven'

try:
    from settings_local import *  # noqa
except Exception:
    pass
