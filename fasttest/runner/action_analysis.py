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

    def __get_variables(self, name):
        '''
        获取变量
        :param name:
        :return:
        '''
        if not re.match(r'^\${(\w+)}$', name):
            raise SyntaxError(name)
        name = name[2:-1]
        if name in self.common_var.keys():
            object_var = self.common_var[name]
        elif name in self.variables:
            object_var = self.variables[name]
        elif name in vars(Var).keys():
            object_var = vars(Var)[name]
        elif Var.extensions_var and name in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][name]
        else:
            object_var = None
        return object_var

    def __join_value(self, contents, join):
        '''
        拼接字符串
        :param contents:
        :param join:
        :return:
        '''
        content_str = None
        if contents:
            for content in contents:
                if content_str:
                    content_str = content_str + join +  self.__replace_string(content)
                else:
                    content_str = self.__replace_string(content)
        else:
            content_str = ''
        return content_str

    def __replace_string(self, content):
        """
        字符串替换
        :param content:
        :return:
        """
        if isinstance(content, str):
            if re.match(r"^'(.*)'$", content):
                content = '"{}"'.format(content)
            elif  re.match(r'^"(.*)"$', content):
                content = "'{}'".format(content)
            else:
                content = '\'{}\''.format(content)
        else:
            content = str(content)
        return content

    def __get_replace_string(self, content):
        '''

        :param content:
        :return:
        '''
        pattern_content = re.compile(r'(\${\w+}+)')
        while True:
            if isinstance(content, str):
                search_contains = re.search(pattern_content, content)
                if search_contains:
                    search_name = self.__get_variables(search_contains.group())
                    if search_name is None:
                        search_name = 'None'
                    elif isinstance(search_name, str):
                        if re.search(r'(\'.*?\')', search_name):
                            search_name = '"{}"'.format(search_name)
                        elif re.search(r'(".*?")', search_name):
                            search_name = '\'{}\''.format(search_name)
                        else:
                            search_name = '\'{}\''.format(search_name)
                    else:
                        search_name = str(search_name)
                    content = content[0:search_contains.span()[0]] + search_name + content[search_contains.span()[1]:]
                else:
                    break
            else:
                content = str(content)
                break

        return content

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
        '''
        获取参数,传参非（）形式
        :param parms:
        :return:
        '''
        parms = parms.strip()
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

    def __get_parm(self, content):
        '''
        获取参数,传参非（）形式
        :param params_str:
        :return:
        '''
        pattern_content = re.compile(r'(\'.*?\'|".*?"|\S+)')
        content_split = re.findall(pattern_content, content)
        contents = []
        for c in content_split:
            var_content = self.__get_params_type(c)
            contents.append(var_content)
        return contents

    def __analysis_exist_parms_keywords(self, step):
        key = step.split('(', 1)[0].strip()
        parms = self.__get_parms(step.lstrip(key))
        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        return action_data

    def __analysis_not_exist_parms_keywords(self, step):
        key = step
        parms = None
        action_data = Dict({
            'key': key,
            'parms': parms,
            'step': step
        })
        return action_data

    def __analysis_setVar_keywords(self, step):
        key = '$.setVar'
        parms = self.__get_parms(step.lstrip('$.setVar'))
        if len(parms) != 2:
            raise SyntaxError(f'"{step}" Missing required parameter key or value!')
        if not isinstance(parms[0], str):
            raise TypeError(f'"{step}" Key must be str, not {type(parms[0])}')
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'setVar',
            'step': step
        })
        return action_data

    def __analysis_variable_keywords(self, step):
        step_split = step.split('=', 1)
        if len(step_split) != 2:
            raise SyntaxError(f'"{step}"')
        elif not step_split[-1].strip():
            raise SyntaxError(f'"{step}"')
        name =  step_split[0].strip()[2:-1]
        var_value = step_split[-1].strip()

        if re.match(r'\$\.(\w)+\(.*\)', var_value):
            key = var_value.split('(', 1)[0]
            if key == '$.id':
                parms = self.__get_replace_string(var_value.split(key, 1)[-1][1:-1])
            elif key == '$.getText':
                parms = self.__get_parms(var_value.split(key, 1)[-1])
            else:
                parms = None
        elif re.match(r'(\w)+\(.*\)', var_value):
            key =  var_value.split('(', 1)[0]
            parms = self.__get_replace_string(var_value.split(key, 1)[-1][1:-1])
        else:
            key = None
            parms = self.__get_parm(var_value)

        action_data = Dict({
            'key': key,
            'parms': parms,
            'name': name,
            'tag': 'getVar',
            'step': step
        })
        return action_data

    def __analysis_common_keywords(self, step, style):
        key = step.split('call', 1)[-1].strip().split('(', 1)[0].strip()
        parms = step.split('call', 1)[-1].strip().split(key, 1)[-1]
        parms = self.__get_parms(parms)
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'call',
            'style': style,
            'step': step
        })
        return action_data

    def __analysis_other_keywords(self, step):
        key = step.split(' ', 1)[0].strip()
        parms = self.__get_replace_string(step.lstrip(key).strip())
        action_data = Dict({
            'key': key,
            'parms': parms,
            'tag': 'other',
            'step': f'{key} {parms}'
        })
        return action_data
        
    def __match_keywords(self, step, style):

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
            return self.__analysis_common_keywords(step, style)
        elif re.match(r'if |elif |while |assert .+', step):
            return self.__analysis_other_keywords(step)
        else:
            raise SyntaxError(f'"{step}"')

    @keywords
    def executor_keywords(self, action, style):

        try:
            if action.tag in ['setVar', 'getVar', 'call', 'other']:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.default_keywords_data.keywords:
                result = self.action_executor.action_executor(action)
            elif action.key in Var.new_keywords_data:
                action.parms = self.__join_value(action.parms, ', ')
                result = self.action_executor.new_action_executor(action)
            else:
                raise KeyError('The {} keyword is undefined!'.format(action.key))

            if action.tag == 'getVar':
                self.variables[action.name] = result
                return result
            else:
                return result
        except Exception as e:
            raise e

    def action_analysis(self, step, style, common):
        log_info(step)
        self.common_var = common
        action_dict = self.__match_keywords(step, style)
        result = self.executor_keywords(action_dict, style)
        return result

if __name__ == '__main__':
    action = ActionAnalysis()


