#!/usr/bin/python
# -*- coding:utf-8 -*-


class Configure(dict):


    def __init__(self, config={}):
        self.__setup_defaults()
        self.update(config)

    def __setup_defaults(self):
        self['log_path'] = '/tmp/earo/'
        self['debug']    = False
        pass

    def __getattr__(self, name):
        return self.get(name, None)
