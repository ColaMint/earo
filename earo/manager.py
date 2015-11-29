#!/usr/bin/python
# -*- coding:utf-8 -*-
from util.local import Local
from Queue import Queue


class Manager:

    __local_defaults = {
        'event_handler_map': dict,
        'handler_queue': Queue,
        'is_comsuming_handler_queue': False
    }

    def __init__(self):
        self.__local = Local(**self.__local_defaults)
        self.__global = self
        self.__global.event_handler_map = {}

    def on(self, event_name, handler, local=False):
        if local:
            if event_name not in self.__local.event_handler_map:
                self.__local.event_handler_map[event_name] = []
            self.__local.event_handler_map[event_name].append(handler)
        else:
            if event_name not in self.__global.event_handler_map:
                self.__global.event_handler_map[event_name] = []
            self.__global.event_handler_map[event_name].append(handler)

    def __find_handlers(self, event_name):
        handlers = []
        if event_name in self.__global.event_handler_map:
            handlers.extend(self.__global.event_handler_map[event_name])
        if event_name in self.__local.event_handler_map:
            handlers.extend(self.__local.event_handler_map[event_name])
        return handlers

    def fire(self, event):
        for handler in self.__find_handlers(event.event_name):
            self.__local.handler_queue.put(handler)
        if not self.__local.is_comsuming_handler_queue:
            self.__local.is_comsuming_handler_queue = True
            while self.__local.handler_queue.qsize() > 0:
                handler = self.__local.handler_queue.get()
                try:
                    handler.handle(event)
                except Exception as e:
                    print e
            self.__local.is_comsuming_handler_queue = False
