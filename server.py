#coding=utf8

from app import app
from cherrypy import wsgiserver
import os
d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer( \
    (app.config['HOST'], app.config['PORT']), d)

if __name__ == '__main__':
    # 每次启动删除临时文件夹文件
    try:
        print "start server ....."
        server.start()
    except KeyboardInterrupt:
        print "stop server ....."
        server.stop()
