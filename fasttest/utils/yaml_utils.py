#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
from fasttest.common import Dict

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
