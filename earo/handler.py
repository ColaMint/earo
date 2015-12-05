#!/usr/bin/python
# -*- coding:utf-8 -*-
import inspect
import traceback


class Handler(object):

    def __init__(self, handle_func):
        self.__check_handle_func(handle_func)
        self.handle_func = handle_func
        self.name = '%s.%s' % (handle_func.__module__, handle_func.__name__)

    def handle(self, event, handler_runtime):
        try:
            handler_runtime.record_begin_time()
            params = self.__build_params(event)
            self.handle_func(**params)
        except Exception as e:
            e.traceback = traceback.format_exc()
            handler_runtime.record_exception(e)
        finally:
            handler_runtime.record_end_time()

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

            args_len = 0 if argspec.args is None else len(argspec.args)
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
