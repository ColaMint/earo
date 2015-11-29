#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.event import Event
from earo.handler import Handler, EventMismatch, HandleFuncParamMissing, InvalidHandleFunc
import unittest

def foo(name, age=15):
    pass

def a1(name, age=15, *args):
    pass

def a2(name, age=15, **kwargs):
    pass

def a3(name, age=15, *args, **kwargs):
    pass

class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_handle_func(self):
        handler = Handler('show', foo)
        self.assertSequenceEqual(handler._Handler__param_list, ['name', 'age'])
        self.assertDictEqual(handler._Handler__param_default, {'age': 15})

    def test_invalid_handle_func(self):
        with self.assertRaises(InvalidHandleFunc):
            handler = Handler('show', a1)
        with self.assertRaises(InvalidHandleFunc):
            handler = Handler('show', a2)
        with self.assertRaises(InvalidHandleFunc):
            handler = Handler('show', a3)

    def test_build_params(self):
        handler = Handler('show', foo)
        event = Event('show', name='k')
        params = handler._Handler__build_params(event)
        self.assertDictEqual(params, {'name': 'k', 'age': 15})

    def test_event_mistmatch(self):
        with self.assertRaises(EventMismatch):
            handler = Handler('show', foo)
            event = Event('display')
            handler.handle(event)

    def test_handle_func_missing(self):
        with self.assertRaises(HandleFuncParamMissing):
            handler = Handler('show', foo)
            event = Event('show')
            handler.handle(event)


if __name__ == '__main__':
    unittest.main()
