#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime
from util.time import datetime_to_str
from util.dictable import Dictable

class HandlerRuntime(Dictable):

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

    @property
    def dict(self):
        runtime = dict()
        runtime['event_name'] = self.event_name
        runtime['begin_time'] = datetime_to_str(
            self.begin_time) if self.begin_time is not None else None
        runtime['end_time'] = datetime_to_str(
            self.end_time) if self.end_time is not None else None
        runtime['time_cost'] = self.time_cost
        runtime['exception'] = {
            'traceback': self.exception.traceback,
            'message': self.exception.message()} if self.exception is not None else None
        runtime['handler'] = self.handler.name
        return runtime
