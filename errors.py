#-*- coding:utf-8 -*-
__author__ = 'fortianwei'
__email__ = 'fortianwei@gmail.com'


class TornassError(StandardError):
    pass

class ConnectionError(TornassError):
    pass

class ClientError(TornassError):
    pass

