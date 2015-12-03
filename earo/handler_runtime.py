#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime


class HandlerRuntime(object):

    def __init__(self, handler, event):
        self.begin_time = None
        self.end_time = None
        self.exception = None
        self.handler = handler
        self.event = event

    def run(self):
        self.handler.handle(self.event, self)

    @property
    def succeeded(self):
        return self.begin_time is not None and self.end_time is not None and self.exception is None

    def record_begin_time(self):
        self.begin_time = datetime.now()

    def record_end_time(self):
        self.end_time = datetime.now()

    def record_exception(self, exception):
        self.exception = exception

    @property
    def time_cost(self):
        if self.begin_time is not None and self.end_time is not None:
            return (self.end_time - self.begin_time).microseconds
        else:
            return -1
