#!/usr/bin/python
# -*- coding:utf-8 -*-
import web

urls = (
    '/', 'oldman'
)

class oldman:
    def GET(self):
        return "Hello world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
