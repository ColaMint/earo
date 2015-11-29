#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from earo.event import Event, BuiltInEventParam
import unittest


class TestEvent(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        event = Event('test', a=1)
        self.assertEqual('test', event.event_name)
        self.assertEqual(1, event.get_param('a', None))
        self.assertEqual(None, event.get_param('b', None))
        self.assertTrue(event.contains_key('a'))
        self.assertFalse(event.contains_key('b'))

    def test_exception(self):
        with self.assertRaises(BuiltInEventParam):
            event = Event('test', a=1, event=3)
        with self.assertRaises(BuiltInEventParam):
            event = Event('test')
            event.set_param('event', 'test')

if __name__ == '__main__':
    unittest.main()
