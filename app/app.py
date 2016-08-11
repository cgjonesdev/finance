from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from urls import app
from logger import logger


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    http_server.debug = True
    ioloop = IOLoop.instance()
    autoreload.start(ioloop)
    ioloop.start()
