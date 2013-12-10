#!/usr/bin/python
#-*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story" + story_id)

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))

class User():
    id = 1
    name = "Ryan"
    addr = "Shanghai"
    def getId(self):
        return 1
    def getName(self):
        return "RyanDoris"
    def getAddr(self):
        return "SH"

class ItemHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        data = {'nick': User()}
        self.render("template.html", title="My title", items=items, **data)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9]+)", StoryHandler),
    (r"/myform", MyFormHandler),
    (r"/item", ItemHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
