#!/usr/bin/python
# -*- coding:utf-8 -*-


class Node:

    def __init__(self):
        self.child_nodes = []

    def add_child_node(self,node):
        self.child_nodes.append(node)


class Tree:

    def __init__(self, root):
        self.root = root


class EventNode(Node):

    def __init__(self, event):
        super(EventNode, self).__init__()
        self.event = event


class HandlerRuntimeNode(None):

    def __init__(self, handler_runtime):
        super(HandlerRuntimeNode, self).__init__()
        self.handler_runtime = handler_runtime


class LogicTree:


    def __init__(self, root):
        super(LogicTree, self).__init__(root)
        self.begin_time = None
        self.end_time   = None
        self.time_cost  = None
        self.event_count = -1
        self.handler_runtime_count = -1
        self.exception_count = -1

    def statistics(self):
        pass
