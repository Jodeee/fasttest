#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import collections

class Dict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key,str):
            raise  KeyError(key)
        return self[str(key)]

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


def analytical_file(path):
    '''
    analytical file
    :param path:
    :return:
    '''
    with open(path, "r", encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        yaml_dict = Dict()
        if yaml_data:
            for key, value in yaml_data.items():
                yaml_dict[key] = value
    return yaml_dict
