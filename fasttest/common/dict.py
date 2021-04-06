#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import collections
try:
    from appium.webdriver import WebElement
except:
    pass
try:
    from macaca.webdriver import WebElement
except:
    pass

class Dict(collections.UserDict):
    def __missing__(self, key):
        return None

    def __contains__(self, item):
        return str(item) in self.data

    def __setitem__(self, key, value):
        if isinstance(value,dict):
            _item = Dict()
            for _key ,_value in value.items():
                _item[_key] = _value
            self.data[str(key)] = _item
        else:
            self.data[str(key)] = value

    def __getattr__(self, item):
        if item in self:
            return self[str(item)]
        else:
            return None
       
    def __copy__(self):
        n_d = type(self)()
        n_d.__dict__.update(self.__dict__)
        return n_d

class DictEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Dict):
            d = {}
            for k, v in obj.items():
                d[k] = v
            return d
        elif isinstance(obj, WebElement):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
