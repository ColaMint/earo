#!/usr/bin/python
# -*- coding:utf-8 -*-


class Configure(dict):
    """
    debug       --  True means setup debug mode, default is False
    log_path    --  the file path to save runtime log, default is '/tmp/earo.log'
    runtime_db  --  the db path to save runtime_tree, default is '/tmp/earo.db'
    """

    def __init__(self, config={}):
        self.__setup_defaults()
        self.update(config)

    def __setup_defaults(self):
        self['debug']    = False
        self['log_path'] = '/tmp/earo.log'
        self['runtime_db'] = '/tmp/earo.db'
        pass

    def __getattr__(self, name):
        return self.get(name, None)
