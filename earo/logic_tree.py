#!/usr/bin/python
# -*- coding:utf-8 -*-
from handler_runtime import HandlerRuntime
from event import Event
from util.time import datetime_to_str
from util.dictable import Dictable, check_dictable


class Node(Dictable):

    def __init__(self, item):
        check_dictable(item)
        self.item = item
        self.child_nodes = list()

    def add_child_node(self, node):
        self.child_nodes.append(node)

    @property
    def type(self):
        return self.item.__class__

    @property
    def dict(self):
        node = dict()
        node['item'] = self.item.dict
        node['type'] = self.item.__class__
        node['child_nodes'] = list()
        for child_node in self.child_nodes:
            node['child_nodes'].append(child_node.dict)
        return node


class Tree(Dictable):

    def __init__(self, root):
        check_dictable(root)
        self.root = root

class LogicTree(Tree):

    def __init__(self, root):
        super(LogicTree, self).__init__(root)
        self.begin_time = None
        self.end_time = None
        self.time_cost = None
        self.event_count = -1
        self.handler_runtime_count = -1
        self.exception_count = -1

    def statistics(self):
        self.event_count = 0
        self.handler_runtime_count = 0
        self.exception_count = 0
        self.__statistics(self.root)
        if self.end_time is not None and self.begin_time is not None:
            self.time_cost = (self.end_time - self.begin_time).microseconds
        else:
            self.time_cost = -1

    def __statistics(self, node):
        if node.type == Event:
            self.event_count += 1
        elif node.type == HandlerRuntime:
            handelr_runtime = node.item
            self.handler_runtime_count += 1
            if handelr_runtime.exception is not None:
                self.exception_count += 1
            if self.begin_time is None or (
                    handelr_runtime.begin_time is not None and handelr_runtime.begin_time < self.begin_time):
                self.begin_time = handelr_runtime.begin_time
            if self.end_time is None or (
                    handelr_runtime.end_time is not None and handelr_runtime.end_time < self.end_time):
                self.end_time = handelr_runtime.end_time
        for child_node in node.child_nodes:
            self.__statistics(child_node)

    @property
    def dict(self):
        tree = dict()
        tree['root'] = self.root.dict
        tree['begin_time'] = datetime_to_str(
            self.begin_time) if self.begin_time is not None else None
        tree['end_time'] = datetime_to_str(
            self.end_time) if self.end_time is not None else None
        tree['time_cost'] = self.time_cost
        tree['event_count'] = self.event_count
        tree['handler_runtime_count'] = self.handler_runtime_count
        tree['exception_count'] = self.exception_count
        return tree
