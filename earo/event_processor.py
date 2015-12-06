#!/usr/bin/python
# -*- coding:utf-8 -*-
from threading import Thread
from event_channel import EventChannel
from runtime_tree import Node, RuntimeTree
from handler_runtime import HandlerRuntime
from util.local import Local
import Queue


class EventProcessor(Thread):

    def __init__(self, id, app, event_channel=None):
        super(EventProcessor, self).__init__()
        self.id = id
        self.__app = app
        self.__event_channel = event_channel
        self.__running = True
        self.__init_local_and_global()

    def __init_local_and_global(self):
        local_defaults = {
            'handler_runtime_node_queue': Queue.Queue,
            'runtime_tree': None,
            'last_handler_runtime_node': None
        }
        self.__local = Local(**local_defaults)

    def run(self):
        self.__app.logger.info('EventProcessor(%d) start working.' % (self.id,))
        event = None
        while self.__running:
            try:
                event = self.__event_channel.get(True, 5)
            except Queue.Empty:
                pass
            if event is not None:
                self.process_event(event)
        self.__app.logger.info('EventProcessor(%d) stop working.' % (self.id,))

    def process_event(self, event):
        event_node = Node(event)
        self.__local.runtime_tree = RuntimeTree(event_node)
        self.__local.last_handler_runtime_node = None
        self.__put_handler_runtime_to_queue_and_add_child_node(event_node)
        while self.__local.handler_runtime_node_queue.qsize() > 0:
            handler_runtime_node = self.__local.handler_runtime_node_queue.get()
            self.__local.last_handler_runtime_node = handler_runtime_node
            handler_runtime = handler_runtime_node.item
            handler_runtime.run(self)
            if handler_runtime.exception is not None:
                self.__app.logger.error(
                    'runtime_tree.id: %s\n%s' %
                    (self.__local.runtime_tree.id,
                        handler_runtime.exception.traceback))
        self.__local.runtime_tree.statistics()
        return self.__local.runtime_tree

    def __put_handler_runtime_to_queue_and_add_child_node(self, event_node):
        for handler in self.__app.find_handlers(event_node.item.event_name):
            handler_runtime = HandlerRuntime(handler, event_node.item)
            handler_runtime_node = Node(handler_runtime)
            event_node.add_child_node(handler_runtime_node)
            self.__local.handler_runtime_node_queue.put(handler_runtime_node)

    def fire(self, event):
        event_node = Node(event)
        self.__put_handler_runtime_to_queue_and_add_child_node(event_node)
        self.__local.last_handler_runtime_node.add_child_node(event_node)

    def stop(self):
        self.__running = False
