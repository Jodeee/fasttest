#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from fasttest.common import log_error
from selenium.common.exceptions import WebDriverException

def check(func, *args, **kwds):
    def wrapper(*args, **kwds):
        index = 10
        result = None
        while index:
            try:
                if args or kwds:
                    result = func(*args, **kwds)
                else:
                    result = func()
                break
            except WebDriverException as e:
                log_error(e.msg, False)
                index -= 1
                if index == 0:
                    raise e
            except Exception as e:
                raise e
        return result
    return wrapper