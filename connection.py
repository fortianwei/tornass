#-*- coding:utf-8 -*-

import socket
import functools

import tornado.ioloop
import tornado.iostream

import errors

class Connection(object):

    #__slots__ = ()
    def __init__(self, host='127.0.0.1', port=8888):
        self.__host = host
        self.__port = port
        self.__stream = None
        self.__is_connected = False
        if isinstance(port, (str, unicode)):
            self.__port = int(port)
        
    @tornado.gen.coroutine
    def connect(self):
        print 'connection connect, host', self.__host, ' port ', str(self.__port)
        if self.__is_connected:
            print 'already connected'
            raise tornado.gen.Return(True) 
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            self.__stream = tornado.iostream.IOStream(s)
            self.__stream.connect((self.__host, self.__port), self._on_connection_established)
        except socket.error, e:
            raise tornado.gen.Return(False)
        except (tornado.gen.Return, StopIteration):
            raise tornado.gen.Return(True)

    def _on_connection_established(self):
        self.__is_connected = True

    @tornado.gen.coroutine
    def send_cmd(self, cmd_list):
        '''send command to socket

        arg: list cmd_list: a list contains the command,just like what in ssdb-cli
             for example: ['multi_hset', 'user', 'name', 'July', 'sex', 'male']
        '''
        if self.__stream.closed():
            self.__close()
            raise errors.ConnectionError('Connection is already closed.')
        cmd_str = self.pack_command(cmd_list)
        self.__stream.write(cmd_str)
        data_received = yield self.__stream.read_until(b'\n\n')
        raise tornado.gen.Return(data_received)

    def pack_command(self, args):
        print 'args is ', str(args)
        cmds = [str(len(arg)) if i % 2 == 0 else arg for arg in args for i in range(2)]
        cmd_str = '\n'.join(cmds) + '\n\n'
        print 'cmd_str is ', cmd_str
        return cmd_str

    @property
    def connected(self):
        return self.__is_connected

    def __del__(self):
        self.__close()
    
    def close(self):
        self.__close()

    def __close(self):
        self.__is_connected = False
        if not self.__stream.closed():
            self.__stream.close()
