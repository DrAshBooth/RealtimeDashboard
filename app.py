import datetime
import time
import random

import tornado.ioloop
import tornado.web
import tornado.websocket

names = ["My Learning", "NEDAP Topup", "GSR"]
people = ["Rob", "Ash", "Rakhee"]


def get_data():
    return {"tile_name": random.choice(names),
            "user": random.choice(people),
            "time": datetime.date.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")}


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dashboard.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args):
        print("WebSocket opened")
        while True:
            data = get_data()
            self.write_message(data)
            time.sleep(random.random()*3)

    def on_message(self, message):
        print("New message {}".format(message))
        self.write_message(message.upper())

    def on_close(self):
        print("Connection closed")


def make_app():
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'}),
        (r'/', DashboardHandler),
        (r'/test', TestHandler),
        (r'/websocket', WebSocketHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()