#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import copy
from typing import Iterable
from fasttest.common import Var, log_info, log_error


class ActionExecutorBase(object):

    def _import(self):
        file_list = []
        try:
            for rt, dirs, files in os.walk(os.path.join(Var.root, "Scripts")):
                for f in files:
                    if f == "__init__.py" or f.endswith(".pyc") or f.startswith(".") or not f.endswith('.py'):
                        continue
                    file_list.append(f'from Scripts.{f[:-3]} import *')
        except Exception as e:
            log_error(' {}'.format(e), False)

        return file_list

    def _out(self, key, result):
        if isinstance(result, list):
            log_info(f' <-- {key}: {type(result)}')
            for l in result:
                log_info(' - {}'.format(l))
        elif isinstance(result, dict):
            log_info(f' <-- {key}: {type(result)}')
            for k, v in result.items():
                log_info(' - {}: {}'.format(k, v))
        else:
            log_info(f' <-- {key}: {type(result)} {result}')

    def _getParms(self, action, index=0, ignore=False):
        parms = action.parms
        if len(parms) <= index or not len(parms):
            if ignore:
                return None
            raise TypeError('missing {} required positional argument'.format(index + 1))
        value = parms[index]
        return value

    def _sleep(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        time.sleep(float(parms))
        return

    def _setVar(self, action):
        '''
        :param action:
        :return:
        '''
        key = self._getParms(action, 0)
        values = self._getParms(action, 1)
        Var.global_var[key] = values
        return

    def _getVar(self, action):
        '''
        :param action:
        :return:
        '''
        key = self._getParms(action, 0)
        if Var.global_var:
            if key in Var.global_var:
                result = Var.global_var[key]
            else:
                result = None
        else:
            result = None
        return result

    def _getLen(self, action):
        '''
        :param action:
        :return:
        '''
        value = self._getParms(action, 0)
        if value:
            return len(value)
        return 0

    def _break(self, action):
        '''
        :param action:
        :return:
        '''
        return True

    def _if(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            log_info(' <-- {}'.format(bool(result)))
            return bool(result)
        except Exception as e:
            raise e

    def _elif(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            log_info(' <-- {}'.format(bool(result)))
            return bool(result)
        except Exception as e:
            raise e

    def _else(self, action):
        '''
        :param action:
        :return:
        '''
        return True

    def _while(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            log_info(' <-- {}'.format(bool(result)))
            return bool(result)
        except Exception as e:
            raise e

    def _for(self, action):
        '''
        :param action:
        :return:
        '''
        items = self._getParms(action, 0)
        value = action.value
        if not isinstance(items, Iterable):
            raise TypeError("'{}' object is not iterable".format(items))
        return {'key': value, 'value': items}

    def _assert(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            log_info(' <-- {}'.format(bool(result)))
            assert result
        except Exception as e:
            raise e

    def _setTimeout(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        Var.time_out = int(parms)

    def _id(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        parms = parms.replace('\n', '')
        result = eval(parms)
        return result

    def _call(self, action):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        func = action.func
        if  not func in Var.common_func.keys():
            raise NameError("name '{}' is not defined".format(func))
        if len(Var.common_func[func].input) != len(parms):
            raise TypeError('{}() takes {} positional arguments but {} was given'.format(func, len(
                Var.common_func[func].input), len(parms)))
        common_var = dict(zip(Var.common_func[func].input, parms))

        try:
            from fasttest.runner.case_analysis import CaseAnalysis
            case = CaseAnalysis()
            case.iteration(Var.common_func[func].steps, '{}  '.format(action.style), common_var)
        except Exception as e:
            # call action中如果某一句step异常，此处会往上抛异常，导致call action也是失败状态，需要标记
            Var.exception_flag = True
            raise e

    def _variable(self, action):
        '''
        调用$.类型方法
        :param action:
        :return:
        '''
        try:
            func = action.func
            if func and func.startswith('$.'):
                func_ = getattr(self, '_{}'.format(func[2:]))
                result = func_(action)
            elif func:
                new_action = action.copy() #todo
                new_action['key'] = action.func
                result = self._new_action_executo(new_action)
            else:
                result = self._getParms(action, 0)
        except Exception as e:
            raise e

        self._out(action.name, result)
        return result

    def _action_executor(self, action):
        '''
        默认关键字
        :param action:
        :return:
        '''
        try:
            func = getattr(self, '_{}'.format(action.key))
        except Exception as e:
            raise NameError("keyword '{}' is not defined".format(action.key))
        result = func(action)
        return result

    def _new_action_executo(self, action, output=True):
        '''
        自定义关键字
        :param action:
        :return:
        '''
        list = self._import()
        for l in list:
            exec(l)
        parms = None
        for index, par in enumerate(action.parms):
            if not parms:
                parms = 'action.parms[{}]'.format(index)
                continue
            parms = '{}, action.parms[{}]'.format(parms, index)
        if not parms:
            result = eval('locals()[action.key]()')
        else:
            result = eval('locals()[action.key]({})'.format(parms))
        if result and output:
            self._out(action.key, result)
        return result
