#!/usr/bin/python
# -*- coding:utf-8 -*-
import inspect
import copy


class Handler:

    def __init__(self, event_name, handle_func):
        self.event_name = event_name
        self.__check_handle_func(handle_func)
        self.handle_func = handle_func

    def handle(self, event):
        if self.event_name != event.event_name:
            raise EventMismatch(event.event_name, self.event_name)
        else:
            self.handle_func(self.__build_params(event))

    def __check_handle_func(self, handle_func):
        if not callable(handle_func):
            raise InvalidHandleFunc('not callable')
        else:
            argspec = inspect.getargspec(handle_func)
            if argspec.varargs is not None:
                raise InvalidHandleFunc(
                    'handle function should not contain varargs')
            if argspec.keywords is not None:
                raise InvalidHandleFunc(
                    'handle function should not contain keywords')

            self.__param_list = []
            self.__param_default = {}

            args_len = 0 if argspec.args is None else len(
                argspec.args)
            defaults_len = 0 if argspec.defaults is None else len(
                argspec.defaults)
            index_offset = args_len - defaults_len
            for i, field in enumerate(argspec.args):
                self.__param_list.append(field)
                default_i = i - index_offset
                if default_i >= 0:
                    self.__param_default[field] = argspec.defaults[default_i]

    def __build_params(self, event):
        params = {}
        for field in self.__param_list:
            if event.contains_key(field):
                params[field] = event.get_param(field)
            else:
                if field in self.__param_default:
                    params[field] = self.__param_default[field]
                else:
                    raise HandleFuncParamMissing(field)
        return params


class EventMismatch(Exception):

    def __init__(self, cur_event_name, target_event_name):
        self.cur_event_name = cur_event_name
        self.target_event_name = target_event_name
        super(
            EventMismatch, self).__init__(
                '[Event Mismatch] cur_event_name: %s, target_event_name: %s.' %
         (cur_event_name, target_event_name))


class HandleFuncParamMissing(Exception):

    def __init__(self, field):
        super(
            HandleFuncParamMissing,
            self).__init__(
                '[Handle Func Param Missing] field : `%s`.' %
         field)


class InvalidHandleFunc(Exception):

    def __init__(self, msg):
        super(
            InvalidHandleFunc,
            self).__init__(
            '[Invalid Handle Function] %s.' %
         msg)
