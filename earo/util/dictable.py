#!/usr/bin/python
# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod

class Dictable(object):

    @property
    @abstractmethod
    def dict(self):pass

class UndictableException(Exception):
    def __init__(self):
        super(
            UndictableException,
            self).__init__(
                '[The instance is undictable]')

def check_dictable(obj):
    if not isinstance(obj, Dictable) :
        raise UndictableException()
