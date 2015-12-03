#!/usr/bin/python
# -*- coding:utf-8 -*-
from util.local import Local
from Queue import Queue
from handler_runtime import HandlerRuntime
from logic_tree import Node, LogicTree


class Manager(object):

    __local_defaults = {
        'event_handler_map': dict,
        'handler_runtime_node_queue': Queue,
        'logic_tree': None,
        'last_handler_runtime_node': None
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
        event_node = Node(event)
        if self.__local.logic_tree is None:
            self.__local.logic_tree = LogicTree(event_node)
        for handler in self.__find_handlers(event.event_name):
            handler_runtime = HandlerRuntime(handler, event)
            handler_runtime_node = Node(handler_runtime)
            event_node.add_child_node(handler_runtime_node)
            self.__local.handler_runtime_node_queue.put(handler_runtime_node)
        if self.__local.last_handler_runtime_node is None:
            while self.__local.handler_runtime_node_queue.qsize() > 0:
                handler_runtime_node = self.__local.handler_runtime_node_queue.get()
                self.__local.last_handler_runtime_node = handler_runtime_node
                handler_runtime_node.item.run()
            self.__local.logic_tree.statistics()
            return self.__local.logic_tree
        else:
            self.__local.last_handler_runtime_node.add_child_node(event_node)
