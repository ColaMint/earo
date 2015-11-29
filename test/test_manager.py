#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.manager import Manager
from earo.handler import Handler
from earo.event import Event
import unittest
from Queue import Queue

names = []

def foo(name):
    names.append('foo-%s' % name)


def boo(name):
    names.append('boo-%s' % name)


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_local(self):
        manager = Manager()
        self.assertDictEqual(manager._Manager__local.event_handler_map, dict())
        self.assertIsInstance(manager._Manager__local.handler_queue, Queue)
        self.assertEqual(
            manager._Manager__local.is_comsuming_handler_queue, False)
        self.assertEqual(manager._Manager__local.unknown, None)

    def test_on_and_find(self):
        manager = Manager()
        handlers = manager._Manager__find_handlers('show')
        self.assertListEqual(handlers, list())

        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        manager.on('show', foo_handler)
        manager.on('show', boo_handler, True)
        handlers = manager._Manager__find_handlers('show')
        self.assertListEqual(handlers, [foo_handler, boo_handler])
        self.assertListEqual(
            manager._Manager__global.event_handler_map['show'],
            [foo_handler])
        self.assertListEqual(
            manager._Manager__local.event_handler_map['show'],
            [boo_handler])

    def test_fire(self):
        manager = Manager()
        foo_handler = Handler(foo)
        boo_handler = Handler(boo)
        manager.on('show', foo_handler)
        manager.on('show', boo_handler, True)
        show_event = Event('show', name = 'A')
        manager.fire(show_event)
        self.assertListEqual(
            names,
            ['foo-A', 'boo-A'])


if __name__ == '__main__':
    unittest.main()
