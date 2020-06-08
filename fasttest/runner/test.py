#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json
from fasttest.common.dict import Dict

def analysis_json(path):
    dict = {}
    with open(os.path.join(path), 'r', encoding='utf-8') as f:
        dict = Dict(json.load(fp=f))
    return dict

def get_parms(step):
    if re.match(' ', step):
        raise SyntaxError(f"'{step}'")
    step = step.strip()
    if re.match(r'\w+\((.*)\)', step):
        key = step.split('(', 1)[0].strip()
        parms = step.lstrip(key)
    elif re.match(r'^\w+$', step):
        key = step
        parms = None
    elif re.match(r'\$\{\w+\}=|\$\{\w+\} =', step):
        step_split = step.split('=', 1)
        if len(step_split) != 2:
            raise SyntaxError(step)
        elif not step_split[-1].strip():
            raise SyntaxError(step)
        var_name = step_split[0].strip()
        var_value = step_split[-1].strip()
        if re.match(r'\$\.(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0]
            parms = var_value.split(key, 1)[-1].strip()
        else:
            key = None
            parms = var_value
        tag ='getVar'
        return

    elif re.match(r'\$\.setVar\(.*\)', step):
        key = '$.setVar'
        parms = step.lstrip('$.setVar')
        tag = 'setVar'
        print()
    elif re.match(r'call \w+\(.*\)', step):
        key = step.split('call', 1)[-1].strip().split('(', 1)[0].strip()
        parms = step.split('call', 1)[-1].strip().split(key, 1)[-1].strip()
        tag = 'call'





def analysis_key(step, dict):
    print(step)

    get_parms(step)

    if re.match(r'\w+\((.*)+\)', step):
        # click(
        print(step)
    elif re.match(r'\w+', step):
        # break
        print(step)
    elif re.match(r'\$\{\w+\}=|\$\{\w+\} =', step):
        # var
        print(step)
    elif re.match(r'call \w+\((.*)+\)', step):
        # call
        print(step)
    elif re.match(r'\$\.(\w)+\(.*\)', step):
        # setVar
        print(step)
    else:
        raise SyntaxError(f"'{step}'")

    if step in dict.keys():
        value = dict[step]
        if value.index:
            print(step)

if __name__ == '__main__':
    dict = analysis_json('keywords.json')
    analysis_key("call getText('df')", dict)