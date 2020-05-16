#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from fasttest.common import Var, Dict, log_info
from fasttest.common.decorator import keywords
from fasttest.runner.action_keyword import ActionKeyWord
from fasttest.runner.action_executor import ActionExecutor

try:
    from Scripts import *
except Exception:
    pass


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
        if Var.common_var and name in Var.common_var.keys():
            object_var = Var.common_var[name]
        elif name in self.variables:
            object_var = self.variables[name]
        elif name in vars(Var).keys():
            object_var = vars(Var)[name]
        elif name in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][name]
        else:
            object_var = None
        return object_var

    def __get_params(self, pattern, content):
        '''
        获取参数,传参以（）形式
        :param params_str:
        :return:
        '''
        content_list = re.split(pattern, content)
        if re.match('^\(.*\)$', content_list[-1]):
            params = []
            pattern_content = re.compile(r'(".*?")|(\'.*?\')|,| ')
            find_content = re.split(pattern_content, content_list[-1][1:-1])
            find_content = [x.strip() for x in find_content if x]
            for param in find_content:
                var_content = self.__get_params_type(param)
                # if not var_content:
                #     raise KeyError(content)
                params.append(var_content)
            return params
        else:
            raise SyntaxError(content)

    def __analysis_params(self, content):
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
            # if not var_content:
            #     raise KeyError(step)
            contents.append(var_content)
        return contents

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
            if re.match(r"^'$", content):
                content = '"{}"'.format(content)
            elif  re.match(r'^"$', content):
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

    def __get_index(self, keyword):
        '''
        获取index
        :param keyword:
        :return:
        '''
        index = keyword.split('@')
        if index and len(index)>1:
            return int(index[1])
        return 0

    @keywords
    def __get_action_step(self, step):
        '''
        获取执行步骤
        :param step:
        :return:
        '''
        action_keyword_list = [ActionKeyWord.INSTALLAPP,
                          ActionKeyWord.UNINSTALLAPP,
                          ActionKeyWord.LAUNCHAPP,
                          ActionKeyWord.CLOSEAPP,
                          ActionKeyWord.TAP,
                          ActionKeyWord.DOUBLETAP,
                          ActionKeyWord.PRESS,
                          ActionKeyWord.ADB,
                          ActionKeyWord.SWIPE,
                          ActionKeyWord.SWIPEUP,
                          ActionKeyWord.SWIPEDOWN,
                          ActionKeyWord.SWIPELEFT,
                          ActionKeyWord.SWIPERIGHT,
                          ActionKeyWord.CLICK,
                          ActionKeyWord.CHECKT,
                          ActionKeyWord.INPUT,
                          ActionKeyWord.IF,
                          ActionKeyWord.ELIF,
                          ActionKeyWord.ELSE,
                          ActionKeyWord.IFCHECK,
                          ActionKeyWord.ELIFCHECK,
                          ActionKeyWord.IFIOS,
                          ActionKeyWord.IFANDROID,
                          ActionKeyWord.WHILE,
                          ActionKeyWord.SLEEP,
                          ActionKeyWord.ASSERT,
                          ActionKeyWord.GOBACK,
                          ActionKeyWord.BREAK,
                                ]
        try:
            action_dict = Dict()
            for action_keyword in action_keyword_list:
                if re.match(r'%s ' % (action_keyword), step) or re.match(r'%s@(\d+|-\d+) ' % (action_keyword), step):
                    action = action_keyword

                    if re.match(r'%s@(\d+|-\d+) ' % (action_keyword), step):
                        step_lift = re.split(r'%s@(\d+|-\d+) ' % (action_keyword), step)[-1].strip()
                    else:
                        step_lift = step.lstrip(action_keyword).strip()

                    if action in ['if', 'elif', 'while', 'assert']:
                        params = self.__get_replace_string(step_lift)
                    else:
                        params = self.__analysis_params(step_lift)

                    action_dict = Dict({
                        'action': action,
                        'params': params,
                    })

                    if action in ['click', 'check', 'input', 'ifcheck', 'elifcheck']:
                        index = self.__get_index(step.split(' ', 1)[0])
                        action_dict['index'] = index

                    log_info(step)
                    
                    action_dict['origin'] = step
                    break

                elif re.match(r'^%s$' % (action_keyword), step):
                    action = step
                    params = None
                    action_dict = Dict({
                        'action': action,
                        'params': params
                    })

                    log_info(step)

                    action_dict['origin'] = step
                    break

            else:
                if re.match(ActionKeyWord.VARIABLES, step):
                    # 赋值
                    step_split = step.split('=', 1)
                    if len(step_split) != 2:
                        raise SyntaxError(step)
                    elif not step_split[-1]:
                        raise SyntaxError(step)
                    action = step_split[0].strip()[2:-1]
                    params = step_split[-1].strip()
                    log_info(step)
                    if re.match(r'\$\.getText', params):
                        # 获取元素text
                        params = self.__get_params(r'\$\.getText', params)
                        from fasttest.runner.action_executor import ActionExecutor
                        action_executor = ActionExecutor()
                        content = action_executor._action_get_text(Dict({'action':'getText', 'params':params}))

                    elif re.match(r'\$\.id', params):
                        # 科学计算
                        params = params.lstrip('$.id')[1:-1]
                        if not params:
                            raise SyntaxError('{} missing 1 required positional argument'.format(step))
                        replace_str = self.__get_replace_string(params)
                        content = eval(replace_str)
                    elif re.match(r'\$\.getGv', params):
                        # 获取全局变量
                        params = self.__get_params(r'\$\.getGv', params)
                        if not len(params):
                            raise SyntaxError('{} missing 1 required positional argument'.format(step))
                        if Var.global_var:
                            if  params[0] in Var.global_var:
                                content = Var.global_var[params[0]]
                            else:
                                content = None
                        else:
                            content = None
                    elif re.match(r'^Scripts.\w+\(.*\)$', params):
                        # 获取脚本返回
                        func = params.split('(', 1)[0].strip()
                        params = self.__get_params(r'^Scripts.\w+', params)
                        join_str = self.__join_value(params, ', ')
                        content = eval('{}({})'.format(func[8:], join_str))
                    else:
                        # 普通赋值
                        content = self.__analysis_params(params)[0]

                    self.variables[action] = content

                    log_info('{} {}: {}'.format(type(self.variables[action]), action, self.variables[action]))

                    action_dict['origin'] = step

                elif re.match(ActionKeyWord.SETGV, step):
                    # 全局变量
                    params = self.__get_params(ActionKeyWord.SETGV, step)
                    if len(params) != 2:
                        raise SyntaxError(step)

                    key = params[0]
                    values = params[1]
                    Var.global_var[key] = values

                    log_info(step)
                    log_info('{} {}: {}'.format(type(Var.global_var[key]), key,  Var.global_var[key]))

                    action_dict = Dict({
                        'origin': step
                    })

                elif re.match(r'%s ' % (ActionKeyWord.CALL), step):
                    # 调用
                    step_split = step.split(ActionKeyWord.CALL, 1)
                    if len(step_split) != 2:
                        raise SyntaxError(step)
                    elif not step_split[-1]:
                        raise SyntaxError(step)

                    func = step_split[-1].split('(')[0].strip()
                    params = self.__get_params(func, step_split[-1].strip())
                    action_dict = Dict({
                        'action': 'call',
                        'origin': step
                    })
                    log_info(step)

                    if re.match(r'^Scripts.\w+\(.*\)$', step_split[-1].strip()):
                        join_str = self.__join_value(params, ', ')
                        action_dict['type'] = 'Scripts'
                        action_dict['func'] = '{}({})'.format(func[8:], join_str)
                    else:
                        Var.common_var = {}
                        if func not in Var.common_func.keys():
                            raise NameError('name "{}" is not defined'.format(func))
                        if len(Var.common_func[func].input) != len(params):
                            raise TypeError('{}() takes {} positional arguments but {} was given'.format(func, len(
                                Var.common_func[func].input), len(params)))
                        Var.common_var = dict(zip(Var.common_func[func].input, params))

                        action_dict['type'] = 'Common'
                        action_dict['func'] = func

                else:
                    raise SyntaxError(step)

            if len(action_dict):
                result = self.action_executor.action_executor(action_dict)
            else:
                result = None
            return result

        except Exception as e:
            raise e

    def action_analysis(self, step):

        result = self.__get_action_step(step)
        return result

if __name__ == '__main__':
    action = ActionAnalysis()
    action.action_analysis('if "name" in ${package}')