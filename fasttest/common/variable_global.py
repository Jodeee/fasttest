#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
class VariableGlobal(object):

    def __getattr__(self, item):
        try:
            name = threading.currentThread().getName()
            value = self.__getattribute__(name)
            return value[item]
        except:
            return None

    def __setattr__(self, key, value):
        name = threading.currentThread().getName()
        try:
            item = self.__getattribute__(name)
        except:
            item = {}
        item.update({key: value})
        object.__setattr__(self, name, item)

    def __setitem__(self, key, value):
        name = threading.currentThread().getName()
        try:
            item = self.__getattribute__(name)
        except:
            item = {}
        item.update({key: value})
        object.__setattr__(self, name, item)

Var = VariableGlobal()