#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class VariableGlobal(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __setattr__(self, key, value):
       object.__setattr__(self,key,value)

    def __setitem__(self, key, value):
        object.__setattr__(self, key, value)

Var = VariableGlobal()