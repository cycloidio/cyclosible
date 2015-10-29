import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import tornado.web
import tornado.websocket
from django.core.wsgi import get_wsgi_application


class CyclosibleWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        # logging.info('Client connected')
        CyclosibleWebSocket.clients.add(self)

    def on_message(self, message):
        # logging.log('Received message')
        CyclosibleWebSocket.broadcast(message)

    def on_close(self):
        # logging.info('Client disconnected')
        if self in CyclosibleWebSocket.clients:
            CyclosibleWebSocket.clients.remove(self)

    @classmethod
    def broadcast(cls, message):
        for client in cls.clients:
            client.write_message(message)


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cyclosible.Cyclosible.settings'
    api = get_wsgi_application()
    application = tornado.web.Application([
        (r'/ws', CyclosibleWebSocket),
        (r'/(.*)', tornado.web.FallbackHandler, dict(
            fallback=tornado.wsgi.WSGIContainer(api)
        ))], debug=True
    )

    tornado.ioloop.IOLoop.instance().start()
    application.listen(80)

if __name__ == "__main__":
    main()
