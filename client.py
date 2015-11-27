#-*- coding:utf-8 -*-

import functools

import tornado.gen

import connection
import errors
#TODO   cmd check str;   use Future(get rid of coroutine)

class Client(object):
    def __init__(self, host='127.0.0.1', port=8888):
        self.__host = host
        self.__port = port
        self.__connection = None

    @tornado.gen.coroutine
    def connect(self):
        self.__connection = connection.Connection(self.__host, self.__port)
        yield self.__connection.connect()

    @property
    def connected(self):
        return self.__connection and self.__connection.connected

    def __getattr__(self, cmd):
        if not hasattr(self, cmd):
            setattr(self, cmd, functools.partial(self.send_cmd, cmd))
        return getattr(self, cmd)

    @tornado.gen.coroutine
    def send_cmd(self, cmd, *args):
        if not self.connected:
            yield self.connect()
        cmd_list = (cmd,) + args
        ret = yield self.__connection.send_cmd(cmd_list)
        recvs = ret.split('\n')[3:-2:2]
        print 'ret is ', recvs

    def on_data_received(self, data):
        print data
        recvs = data.split('\n')[3:-2:2]
        print 'recvs, ', recvs
        stream.close()
        tornado.ioloop.IOLoop.current().stop()

    @tornado.gen.coroutine
    def test(self):
        print 'x is '
        x = yield self.get('b')
        y = yield self.set('c', '2')
        z = yield self.get('c')

if __name__ == '__main__':
    client = Client()
    client.test()
    tornado.ioloop.IOLoop.current().start()
    
