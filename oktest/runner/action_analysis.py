#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from oktest.common import Var, Dict
from oktest.runner.action_keyword import ActionKeyWord

try:
    from Scripts import *
except Exception:
    pass


class ActionAnalysis(object):

    def __init__(self):
        self.variables = {}

    def __get_varname(self, var):
        """
        获取变量名称
        :param var:
        :return:
        """
        pattern_var = re.compile(r'\${(\w+)}')
        pattern_all = re.compile(r'\${(.*?)}')
        varname = re.findall(pattern_var, str(var))
        all_varname = re.search(pattern_all, str(var))
        if all_varname and not varname:
            raise SyntaxError(var)
        return varname

    def __get_variables(self, varname):
        """
        获取变量
        :param varname:
        :return:
        """
        find_var = self.__get_varname(varname)
        if not find_var:
            return varname
        elif len(find_var) > 1:
            raise SyntaxError(varname)
        elif "${%s}" % find_var[0] != varname:
            raise SyntaxError(varname)

        find_var = find_var[0]
        if Var.common_var and find_var in Var.common_var.keys():
            object_var = Var.common_var[find_var]
        elif find_var in self.variables:
            object_var = self.variables[find_var]
        elif find_var in vars(Var).keys():
            object_var = vars(Var)[find_var]
        elif find_var in Var.extensions_var['variable'].keys():
            object_var = Var.extensions_var['variable'][find_var]
        else:
            object_var = None
        return object_var

    def __set_variables(self, content):
        """
        处理value
        直接赋值(${test} = content)，包括：test、'test'、"test"、"'test'"、'"test"'、1、True
        间接赋值(${test} = ${content}),无需处理数据类型
        :param content:
        :return:
        """
        if content.startswith('\'') and content.endswith('\''):
            content = '{}'.format(content.strip('\''))
        elif content.startswith('"') and content.endswith('"'):
            content = '{}'.format(content.strip('"'))
        elif re.search(r'(\${\w+}?)', content):
            search_name = self.__get_variables(content)
            content = search_name
        else:
            try:
                content = eval(content)
            except:
                content = content
        return content

    def __replace_string(self, content):
        """
        origin_step 替换
        :param content:
        :return:
        """
        if content is None:
            return None
        if isinstance(content, int):
            content = str(content)
        elif isinstance(content, bool):
            content = str(content)
        elif isinstance(content, str):
            if content.startswith('\'') and content.endswith('\''):
                content = '"{}"'.format(content)
            elif content.startswith('"') and content.endswith('"'):
                content = "'{}'".format(content)
            else:
                content = '\'{}\''.format(content)
        return content

    def __get_contents(self, content):
        """
        获取()中参数
        :return:
        """
        pattern_content = re.compile(r'\((.*)\)')
        find_content = re.findall(pattern_content, content)
        if not find_content:
            raise SyntaxError(find_content)
        find_content = find_content[0]
        pattern_content = re.compile(r'(".*?")|(\'.*?\')|,')
        find_content = re.split(pattern_content, find_content)
        find_content = [x.strip() for x in find_content if x]
        find_content = [self.__set_variables(x) for x in find_content if x]
        return find_content

    def __get_content(self, content):
        """
        获取参数，非()形式
        :param content:
        :return:
        """
        pattern_content = re.compile(r'(\'.*?\'|".*?"|\S+)')
        content_split = re.findall(pattern_content, content)
        contents = []
        for content in content_split:
            var_content = self.__set_variables(content)
            if not var_content:
                raise KeyError(content)
            contents.append(var_content)
        return contents

    def __get_origincontent(self, content):
        """
        获取原语句
        :param content:
        :return:
        """
        pattern_content = re.compile(r'(\'.*?\'|".*?"|\S+)')
        content_split = re.findall(pattern_content, content)
        contents = []
        for content in content_split:
            pattern_content = re.compile(r'(\${\w+}+)')
            isVar_content = re.search(pattern_content, content)
            content = self.__get_variables(content)
            if isVar_content:
                content = self.__replace_string(content)
            contents.append(content)
        return ' '.join(contents)

    def __get_index(self, keyword):
        """
        :param content:
        :return:
        """
        index = keyword.split('@')
        if index and len(index)>1:
            return int(index[1])
        return 0

    def __get_keyword(self, keywords, step):
        """
        匹配关键字
        :param keywords:
        :param step:
        :return:
        """
        pattern_keywords = re.compile(r'{}@(\d|-\d)+ '.format(keywords))
        match_keywords_index = re.match(pattern_keywords, step)
        match_keywords = re.match(r'{} '.format(keywords), step)
        if match_keywords_index:
            return match_keywords_index.group().strip()
        elif match_keywords:
            return match_keywords.group().strip()
        else:
            raise SyntaxError(step)

    def __join_value(self, contents, join):
        """
        拼接字符串 var call
        :param contents:
        :return:
        """
        content_str = None
        if contents:
            for content in contents:
                if content_str:
                    content_str = content_str + join +  (self.__replace_string(content) if content else 'None')
                else:
                    content_str = self.__replace_string(content) if content else 'None'
        else:
            content_str = ''
        return content_str

    def __get_replace_string(self, content):
        """
        替换变量
        ${num} = 1
        if ${num} == 1
        if 1 == 1
        :param content:
        :return:
        """
        if content is None:
            return 'None'
        pattern_content = re.compile(r'(\${\w+}+)')
        while True:
            if isinstance(content, str):
                search_contains = re.search(pattern_content, content)
                if search_contains:
                    search_name = self.__get_variables(search_contains.group())
                    if isinstance(search_name, int):
                        search_name = str(search_name)
                    elif isinstance(search_name, bool):
                        search_name = str(search_name)
                    elif isinstance(search_name, str):
                        if re.search(r'(\'.*?\')', search_name):
                            search_name = '"{}"'.format(search_name)
                        elif re.search(r'(".*?")', search_name):
                            search_name = '\'{}\''.format(search_name)
                        else:
                            search_name = '\'{}\''.format(search_name)
                    elif not  search_name:
                        search_name = 'None'

                    content = content[0:search_contains.span()[0]] + search_name + content[search_contains.span()[1]:]
                else:
                    break
            else:
                break

        return content

    def __action_variables(self, step):
        """
        变量
        :param step:
        :return:
        """
        step_split = step.split('=', 1)
        if len(step_split) != 2:
            raise SyntaxError(step)
        elif not step_split[-1]:
            raise SyntaxError(step)
        var_name = self.__get_varname(step_split[0].strip())[0]
        var_content = step_split[-1].strip()
        origin_content = var_content
        if re.match(r'\$\.getText', var_content):
            var_step = self.__action_getText(var_content)
            from oktest.runner.action_executor import ActionExecutor
            action = ActionExecutor()
            var_content = action._action_getText(var_step)
        elif re.match(ActionKeyWord.SCRIPTS, var_content):
            scripts_func = var_content.split('(')[0]
            scripst_content = self.__get_contents(var_content)
            scripst_content = self.__join_value(scripst_content, ',')
            var_content = eval('{}({})'.format(scripts_func[8:], scripst_content))
        elif re.match(r'\$\.id', var_content):
            pattern_content = re.compile(r'\((.*)\)')
            id_content = re.findall(pattern_content, var_content)
            if not id_content:
                raise SyntaxError(step)
            id_content = id_content[0]
            id_content = self.__get_replace_string(id_content)
            var_content = eval(id_content)
        elif re.match(r'\$\.getGV', var_content):
            getGV_content = self.__get_contents(var_content)
            if len(getGV_content) != 1:
                raise SyntaxError(step)
            getGV_content = getGV_content[0]
            if getGV_content in Var.global_var:
                var_content = Var.global_var[getGV_content]
            else:
                var_content = None
        elif re.match(r'\$\.getPosition', var_content):
            pass
        else:
            var_content = self.__set_variables(var_content)

        self.variables[var_name] = var_content
        if var_content is not None:
            origin_step = '{}'.format(step.replace(origin_content, self.__replace_string(var_content)))
        else:
            origin_step = '{}None'.format(step.rstrip(origin_content))

        action_dict = Dict({
            'action': 'variables',
            'content': var_content,
            'origin_step': origin_step
        })
        return action_dict

    def __action_call(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.CALL).strip()
        if not origin_content:
            raise SyntaxError(step)
        call_func = origin_content.split('(')[0]
        call_content = self.__get_contents(origin_content)
        if origin_content.startswith(ActionKeyWord.SCRIPTS):
            call_type = ActionKeyWord.SCRIPTS
            call_content = self.__join_value(call_content, ',')
            call_func = '{}({})'.format(call_func, call_content)
            origin_step = 'call {}'.format(call_func)
            call_func = call_func[8:]
        else:
            call_type = ActionKeyWord.COMMON
            Var.common_var = {}
            if call_func not in Var.common_func.keys():
                raise NameError('name "{}" is not defined'.format(call_func))
            if len(Var.common_func[call_func].input) != len(call_content):
                raise TypeError('{}() takes {} positional arguments but {} was given'.format(call_func, len(
                    Var.common_func[call_func].input), len(call_content)))
            Var.common_var = dict(zip(Var.common_func[call_func].input, call_content))
            object_content = self.__join_value(call_content, ',')
            origin_step = "call {}({})".format(call_func, object_content)

        action_dict = Dict({
            'action': ActionKeyWord.CALL,
            'type': call_type,
            'func': call_func,
            'origin_step': origin_step
        })
        return action_dict

    def __action_startApp(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.STARTAPP).strip()
        startApp_content = self.__get_content(origin_content)
        if len(startApp_content) > 1:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.STARTAPP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.STARTAPP,
            'activity': startApp_content[0] if startApp_content else '',
            'origin_step': origin_step
        })
        return action_dict

    def __action_stopApp(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.STOPAPP).strip()
        stopApp_content = self.__get_content(origin_content)
        if len(stopApp_content) > 1:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.STARTAPP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.STOPAPP,
            'package': stopApp_content[0] if stopApp_content else '',
            'origin_step': origin_step
        })
        return action_dict

    def __action_tap(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.TAP).strip()
        tap_content = self.__get_content(origin_content)
        if len(tap_content) != 2:
            raise SyntaxError(step)
        x, y = tap_content
        origin_step = '{} {}'.format(ActionKeyWord.TAP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.TAP,
            'location': {
                'x': int(x),
                'y': int(y)
            },
            'origin_step': origin_step
        })
        return action_dict

    def __action_doubleTap(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.DOUBLETAP).strip()
        doubleTap_content = self.__get_content(origin_content)
        if len(doubleTap_content) != 2:
            raise SyntaxError(step)
        x, y = doubleTap_content
        origin_step = '{} {}'.format(ActionKeyWord.DOUBLETAP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.DOUBLETAP,
            'location': {
                'x': int(x),
                'y': int(y)
            },
            'origin_step': origin_step
        })
        return action_dict

    def __action_press(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.PRESS).strip()
        press_content = self.__get_content(origin_content)
        if len(press_content) == 2:
            x, y = press_content
            s = 3
        elif len(press_content) == 3:
            x, y, s = press_content
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.PRESS, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.PRESS,
            'location': {
                'x': int(x),
                'y': int(y)
            },
            'duration': int(s),
            'origin_step': origin_step
        })
        return action_dict

    def __action_swipeUp(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SWIPEUP).strip()
        swipeUp_content = self.__get_content(origin_content)
        if not swipeUp_content:
            during = 3
        elif len(swipeUp_content) == 1:
            during = swipeUp_content[0]
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.SWIPEUP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SWIPEUP,
            'during': int(during),
            'origin_step': origin_step
        })
        return action_dict

    def __action_swipeDown(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SWIPEDOWN).strip()
        swipeDown_content = self.__get_content(origin_content)
        if not swipeDown_content:
            during = 3
        elif len(swipeDown_content) == 1:
            during = swipeDown_content[0]
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.SWIPEDOWN, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SWIPEDOWN,
            'during': int(during),
            'origin_step': origin_step
        })
        return action_dict

    def __action_swipeLeft(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SWIPELEFT).strip()
        swipeLeft_content = self.__get_content(origin_content)
        if not swipeLeft_content:
            during = 3
        elif len(swipeLeft_content) == 1:
            during = swipeLeft_content[0]
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.SWIPELEFT, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SWIPELEFT,
            'during': int(during),
            'origin_step': origin_step
        })
        return action_dict

    def __action_swipeRight(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SWIPERIGHT).strip()
        swipeRight_content = self.__get_content(origin_content)
        if not swipeRight_content:
            during = 3
        elif len(swipeRight_content) == 1:
            during = swipeRight_content[0]
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.SWIPERIGHT, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SWIPERIGHT,
            'during': int(during),
            'origin_step': origin_step
        })
        return action_dict

    def __action_swipe(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SWIPE).strip()
        swipe_content = self.__get_content(origin_content)
        if len(swipe_content) == 4:
            during = 3
            fromx, fromy, tox, toy = swipe_content
        elif len(swipe_content) == 5:
            fromx, fromy, tox, toy, during = swipe_content
        else:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.SWIPE, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SWIPE,
            'location': {
                'fromx': int(fromx),
                'fromy': int(fromy),
                'tox': int(tox),
                'toy': int(toy)
            },
            'during': int(during),
            'origin_step': origin_step
        })
        return action_dict

    def __action_goBack(self, step):
        """
        :param step:
        :return:
        """
        action_dict = Dict({
            'action': ActionKeyWord.GOBACK,
            'cmd': 'shell input keyevent 4',
            'origin_step': ActionKeyWord.GOBACK
        })
        return action_dict

    def __action_adb(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.ADB).strip()
        adb_content = self.__get_content(origin_content)
        if len(adb_content) != 1:
            raise SyntaxError(step)
        origin_step = '{} {}'.format(ActionKeyWord.ADB, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.ADB,
            'cmd': adb_content[0],
            'origin_step': origin_step
        })
        return action_dict

    def __action_click(self, step):
        """
        :param step:
        :return:
        """
        keyword = self.__get_keyword(ActionKeyWord.CLICK, step)
        origin_content = step.lstrip(keyword).strip()
        click_index = self.__get_index(keyword)
        click_content = self.__get_content(origin_content)
        if len(click_content) != 1:
            raise SyntaxError(step)
        origin_step = "{} {}".format(keyword, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.CLICK,
            'element': click_content[0],
            'index': click_index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_check(self, step):
        """
        :param step:
        :return:
        """
        keyword = self.__get_keyword(ActionKeyWord.CHECKT, step)
        origin_content = step.lstrip(keyword).strip()
        check_index = self.__get_index(keyword)
        check_content = self.__get_content(origin_content)
        if len(check_content) != 1:
            raise SyntaxError(step)
        origin_step = "{} {}".format(keyword, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.CHECKT,
            'element': check_content[0],
            'index': check_index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_input(self, step):
        """
        :param step:
        :return:
        """
        keyword = self.__get_keyword(ActionKeyWord.INPUT, step)
        origin_content = step.lstrip(keyword).strip()
        input_index = self.__get_index(keyword)
        input_content = self.__get_content(origin_content)
        if len(input_content) != 2:
            raise SyntaxError(step)
        origin_step = "{} {}".format(keyword, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.INPUT,
            'element': input_content[0],
            'content': input_content[1],
            'index': input_index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_getText(self, step):
        """
        :param step:
        :return:
        """
        getText_content = self.__get_contents(step)
        origin_content = self.__join_value(getText_content, ',')

        if len(getText_content) == 1:
            index = 0
        elif len(getText_content) == 2:
            index = int(getText_content[-1])
        else:
            raise SyntaxError(step)
        origin_step = "$.getText({})".format(origin_content)
        action_dict = Dict({
            'action': ActionKeyWord.GETTEXT,
            'element': getText_content[0],
            'index': index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_if(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.IF).strip()
        if_content = self.__get_replace_string(origin_content)
        origin_step = '{} {}'.format(ActionKeyWord.IF, if_content)
        action_dict = Dict({
            'action': ActionKeyWord.IF,
            'content': if_content,
            'origin_step': origin_step
        })
        return action_dict

    def __action_elif(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.ELIF).strip()
        elif_content = self.__get_replace_string(origin_content)
        origin_step = '{} {}'.format(ActionKeyWord.ELIF, elif_content)
        action_dict = Dict({
            'action': ActionKeyWord.ELIF,
            'content': elif_content,
            'origin_step': origin_step
        })
        return action_dict

    def __action_ifcheck(self, step):
        """
        :param step:
        :return:
        """
        keyword = self.__get_keyword(ActionKeyWord.IFCHECK, step)
        origin_content = step.lstrip(keyword).strip()
        ifcheck_index = self.__get_index(keyword)
        ifcheck_content = self.__get_content(origin_content)
        if len(ifcheck_content) != 1:
            raise SyntaxError(step)
        origin_step = "{} {}".format(keyword, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.IFCHECK,
            'element': ifcheck_content[0],
            'index': ifcheck_index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_elifcheck(self, step):
        """
        :param step:
        :return:
        """
        keyword = self.__get_keyword(ActionKeyWord.ELIFCHECK, step)
        origin_content = step.lstrip(keyword).strip()
        elifcheck_index = self.__get_index(keyword)
        elifcheck_content = self.__get_content(origin_content)
        if len(elifcheck_content) != 1:
            raise SyntaxError(step)
        origin_step = "{} {}".format(keyword, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.ELIFCHECK,
            'element': elifcheck_content[0],
            'index': elifcheck_index,
            'origin_step': origin_step
        })
        return action_dict

    def __action_ifiOS(self, step):
        """
        :param step:
        :return:
        """
        action_dict = Dict({
            'action': ActionKeyWord.IFIOS,
            'origin_step': ActionKeyWord.IFIOS
        })
        return action_dict

    def __action_ifAndroid(self, step):
        """
        :param step:
        :return:
        """
        action_dict = Dict({
            'action': ActionKeyWord.IFANDROID,
            'origin_step': ActionKeyWord.IFANDROID
        })
        return action_dict

    def __action_else(self, step):
        """
        :param step:
        :return:
        """
        if len(step.strip()) != 4:
            raise SyntaxError(step)
        action_dict = Dict({
            'action': ActionKeyWord.ELSE,
            'origin_step': ActionKeyWord.ELSE
        })
        return action_dict

    def __action_sleep(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.SLEEP).strip()
        sleep_content = self.__get_content(origin_content)
        if len(sleep_content) != 1:
            raise SyntaxError(step)
        duration = int(sleep_content[0])
        origin_step = '{} {}'.format(ActionKeyWord.SLEEP, self.__get_origincontent(origin_content))
        action_dict = Dict({
            'action': ActionKeyWord.SLEEP,
            'duration': duration,
            'origin_step': origin_step
        })
        return action_dict

    def __action_assert(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.ASSERT).strip()
        assert_content = self.__get_replace_string(origin_content)
        origin_step = '{} {}'.format(ActionKeyWord.ASSERT, assert_content)
        action_dict = Dict({
            'action': ActionKeyWord.ASSERT,
            'content': assert_content,
            'origin_step': origin_step
        })
        return action_dict

    def __action_while(self, step):
        """
        :param step:
        :return:
        """
        origin_content = step.lstrip(ActionKeyWord.WHILE).strip()
        while_content = self.__get_replace_string(origin_content)
        origin_step = '{} {}'.format(ActionKeyWord.WHILE, while_content)
        action_dict = Dict({
            'action': ActionKeyWord.WHILE,
            'content': while_content,
            'origin_step': origin_step
        })
        return action_dict

    def __action_break(self, step):
        """
        :param step:
        :return:
        """
        if len(step.strip()) != 5:
            raise SyntaxError(step)
        action_dict = Dict({
            'action': ActionKeyWord.BREAK,
            'origin_step': ActionKeyWord.BREAK
        })
        return action_dict

    def __action_setGV(self, step):
        """
        设置全局变量
        :param step:
        :return:
        """
        setGV_content = self.__get_contents(step)
        origin_content = self.__join_value(setGV_content, ',')
        if len(setGV_content) != 2:
            raise SyntaxError(step)
        key = setGV_content[0]
        values = setGV_content[1]
        Var.global_var[key] = values
        origin_step = "$.setGV({})".format(origin_content)
        action_dict = Dict({
            'action': 'setGV',
            'origin_step': origin_step
        })
        return action_dict

    def action_analysis(self, step):
        """
        :param step:
        :return:
        """
        if re.match(ActionKeyWord.VARIABLES, step):
            action = self.__action_variables(step)

        elif re.match(ActionKeyWord.CALL, step):
            action = self.__action_call(step)

        elif re.match(ActionKeyWord.STARTAPP, step):
            action = self.__action_startApp(step)

        elif re.match(ActionKeyWord.STOPAPP, step):
            action = self.__action_stopApp(step)

        elif re.match(ActionKeyWord.TAP, step):
            action = self.__action_tap(step)

        elif re.match(ActionKeyWord.DOUBLETAP, step):
            action = self.__action_doubleTap(step)

        elif re.match(ActionKeyWord.PRESS, step):
            action = self.__action_press(step)

        elif re.match(ActionKeyWord.SWIPEUP, step):
            action = self.__action_swipeUp(step)

        elif re.match(ActionKeyWord.SWIPEDOWN, step):
            action = self.__action_swipeDown(step)

        elif re.match(ActionKeyWord.SWIPELEFT, step):
            action = self.__action_swipeLeft(step)

        elif re.match(ActionKeyWord.SWIPERIGHT, step):
            action = self.__action_swipeRight(step)

        elif re.match(ActionKeyWord.SWIPE, step):
            action = self.__action_swipe(step)

        elif re.match(ActionKeyWord.GOBACK, step):
            action = self.__action_goBack(step)

        elif re.match(ActionKeyWord.ADB, step):
            action = self.__action_adb(step)

        elif re.match(ActionKeyWord.CLICK, step):
            action = self.__action_click(step)

        elif re.match(ActionKeyWord.CHECKT, step):
            action = self.__action_check(step)

        elif re.match(ActionKeyWord.INPUT, step):
            action = self.__action_input(step)

        elif re.match(ActionKeyWord.IFCHECK, step):
            action = self.__action_ifcheck(step)

        elif re.match(ActionKeyWord.ELIFCHECK, step):
            action = self.__action_elifcheck(step)

        elif re.match(ActionKeyWord.IFIOS, step):
            action = self.__action_ifiOS(step)

        elif re.match(ActionKeyWord.IFANDROID, step):
            action = self.__action_ifAndroid(step)

        elif re.match(ActionKeyWord.IF, step):
            action = self.__action_if(step)

        elif re.match(ActionKeyWord.ELIF, step):
            action = self.__action_elif(step)

        elif re.match(ActionKeyWord.ELSE, step):
            action = self.__action_else(step)

        elif re.match(ActionKeyWord.SLEEP, step):
            action = self.__action_sleep(step)

        elif re.match(ActionKeyWord.ASSERT, step):
            action = self.__action_assert(step)

        elif re.match(ActionKeyWord.WHILE, step):
            action = self.__action_while(step)

        elif re.match(ActionKeyWord.BREAK, step):
            action = self.__action_break(step)

        elif re.match(ActionKeyWord.SETGV, step):
            action = self.__action_setGV(step)
        else:
            raise SyntaxError(step)

        return action