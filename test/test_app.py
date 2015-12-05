#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.app import App
from earo.handler import Handler
from earo.event import Event
from earo.runtime_tree import Node, RuntimeTree
import unittest
from Queue import Queue
import sys

names = []

config = {
    'debug': True,
    'log_path': '/tmp/test.log'
}

def foo(name):
    names.append('foo-%s' % name)


def boo(name):
    names.append('boo-%s' % name)


def eoo(name):
    names.append('eoo-%s' % name)
    raise Exception('eoo')


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config(self):
        app = App('test_config', config)
        self.assertEqual(True, app.config.debug)
        self.assertEqual('/tmp/test.log', app.config.log_path)
        self.assertEqual(None, app.config.unknown)

    def test_local(self):
        app = App('test_local', config)
        self.assertDictEqual(app._App__local.event_handler_map, dict())
        self.assertIsInstance(
            app._App__local.handler_runtime_node_queue, Queue)
        self.assertEqual(
            app._App__local.runtime_tree, None)
        self.assertEqual(app._App__local.unknown, None)

    def test_on_and_find(self):
        app = App('test_on_and_find', config)
        handlers = app._App__find_handlers('show')
        self.assertListEqual(handlers, list())

        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        handlers = app._App__find_handlers('show')
        self.assertListEqual(handlers, [foo_handler, boo_handler])
        self.assertListEqual(
            app._App__global.event_handler_map['show'],
            [foo_handler])
        self.assertListEqual(
            app._App__local.event_handler_map['show'],
            [boo_handler])

    def test_fire(self):
        app = App('test_fire', config)
        def fire():
            names.append('fire')
            event = Event('display', name='B')
            app.fire(event)
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        eoo_handler = Handler(eoo)
        fire_handler = Handler(fire)
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        app.on('show', fire_handler, True)
        app.on('display', eoo_handler)
        show_event = Event('show', name='A')
        runtime_tree = app.fire(show_event)
        self.assertListEqual(
            names,
            ['foo-A', 'boo-A', 'fire', 'eoo-B'])
        self.assertEqual(runtime_tree.event_count, 2)
        self.assertEqual(runtime_tree.handler_runtime_count, 4)
        self.assertEqual(runtime_tree.exception_count, 1)
        self.assertNotEqual(runtime_tree.begin_time, None)
        self.assertNotEqual(runtime_tree.end_time, None)
        self.assertNotEqual(runtime_tree.time_cost, -1)

    def test_pickle(self):
        app = App('test_pickle', config)
        def fire():
            names.append('fire')
            event = Event('display', name='B')
            app.fire(event)
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        eoo_handler = Handler(eoo)
        fire_handler = Handler(fire)
        app.on('show', foo_handler)
        app.on('show', boo_handler, True)
        app.on('show', fire_handler, True)
        app.on('display', eoo_handler)
        show_event = Event('show', name='A')
        runtime_tree = app.fire(show_event)
        self.assertDictEqual(
            RuntimeTree.loads(
                runtime_tree.dumps()),
         runtime_tree.dict)

if __name__ == '__main__':
    unittest.main()
