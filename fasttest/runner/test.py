#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import json
from fasttest.common import Var, Dict, log_info
from fasttest.common.decorator import keywords
from fasttest.runner.action_executor import ActionExecutor

class ActionAnalysis(object):

    def __init__(self):
        self.variables = {}
        self.action_executor = ActionExecutor()

    def __analysis_json(self, path):
        dict = {}
        with open(os.path.join(path), 'r', encoding='utf-8') as f:
            dict = Dict(json.load(fp=f))
        return dict

    def __get_variables(self, name):
        '''
        获取变量
        :param name:
        :return:
        '''
        if not re.match(r'^\${(\w+)}$', name):
            raise SyntaxError(name)
        name = name[2:-1]
        if Var.common_var and name in Var.common_var.keys():
            object_var = Var.common_var[name]
        elif name in self.variables:
            object_var = self.variables[name]
        elif name in vars(Var).keys():
            object_var = vars(Var)[name]
        elif Var.extensions_var and name in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][name]
        else:
            object_var = None
        return object_var

    def __get_params_type(self, param):
        '''
        获取参数类型
        :param param:
        :return:
        '''
        if re.match(r"^'$", param):
            param = param.strip("'")
        elif re.match(r'^"$', param):
            param = param.strip('"')
        elif re.search(r'(^\${\w+}?$)', param):
            param = self.__get_variables(param)
        else:
            try:
                param = eval(param)
            except:
                param = param
        return param

    def __get_parms(self, parms):

        if re.match('^\(.*\)$', parms):
            params = []
            pattern_content = re.compile(r'(".*?")|(\'.*?\')|,| ')
            find_content = re.split(pattern_content, parms[1:-1])
            find_content = [x.strip() for x in find_content if x]
            for param in find_content:
                var_content = self.__get_params_type(param)
                params.append(var_content)
            return params
        else:
            raise SyntaxError(parms)

    def __analysis_exist_parms_keywords(self, step):
        key = step.split('(', 1)[0].strip()
        parms = self.__get_parms(step.lstrip(key))
        action_data = Dict({
            'key': key,
            'parms': parms
        })
        return action_data

    def __analysis_not_exist_parms_keywords(self, step):
        key = step
        parms = None
        action_data = Dict({
            'key': key,
            'parms': parms
        })
        return action_data

    def __analysis_setVar_keywords(self, step):
        key = '$.setVar'
        parms = self.__get_parms(step.lstrip('$.setVar'))
        if len(parms) != 2:
            raise SyntaxError(f'"{step}"')
        if not isinstance(parms[0], str):
            raise SyntaxError(f'"{step}"')
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'setVar'
        })
        return action_data

    def __analysis_variable_keywords(self, step):
        step_split = step.split('=', 1)
        if len(step_split) != 2:
            raise SyntaxError(f'"{step}"')
        elif not step_split[-1].strip():
            raise SyntaxError(f'"{step}"')
        name = step_split[0].strip()
        var_value = step_split[-1].strip()

        if re.match(r'^\w+\(.*\)', var_value):
            raise SyntaxError(f'"{step}"')
        if re.match(r'\$\.(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0]
            parms = self.__get_parms(var_value.split(key, 1)[-1].strip())
        else:
            key = None
            parms = var_value

        action_data = Dict({
            'key': key,
            'parms': parms,
            'name': name,
            'tag': 'getVar'
        })
        return action_data

    def __analysis_common_keywords(self, step):
        key = step.split('call', 1)[-1].strip().split('(', 1)[0].strip()
        parms = step.split('call', 1)[-1].strip().split(key, 1)[-1].strip()
        parms = self.__get_parms(parms)
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'call'
        })
        return action_data
        
    def match_keywords(self, step):

        if re.match(' ', step):
            raise SyntaxError(f'"{step}"')
        step = step.strip()

        if re.match(r'\w+\((.*)\)', step):
            return self.__analysis_exist_parms_keywords(step)
        elif re.match(r'^\w+$', step):
            return self.__analysis_not_exist_parms_keywords(step)
        elif re.match(r'\$\{\w+\}=|\$\{\w+\} =', step):
            return self.__analysis_variable_keywords(step)
        elif re.match(r'\$\.setVar\(.*\)', step):
            return self.__analysis_setVar_keywords(step)
        elif re.match(r'call \w+\(.*\)', step):
            return self.__analysis_common_keywords(step)
        else:
            raise SyntaxError(f'"{step}"')

    # if step in dict.keys():
    #     value = dict[step]
    #     if value.index:
    #         print(step)

if __name__ == '__main__':
    action = ActionAnalysis()
    # dict = action.__analysis_json('keywords.json')
    action_dict = action.match_keywords("call getst('1',1)")
    print(action_dict)
