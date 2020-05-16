#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import sys
import time
import traceback
import threading
from macaca.webdriver import WebElement
from fasttest.common import *

def therading(func):
    def start(*args, **kwds):
        def run():
            try:
                th.ret = func(*args, **kwds)
            except:
                th.exc = sys.exc_info()
        def get(timeout=None):
            th.join(timeout)
            if th.exc:
                raise th.exc[1]
            return th.ret
        th = threading.Thread(None,run)
        th.exc = None
        th.ret = None
        th.get = get
        th.start()
        return th
    return start

def keywords(func, *args, **kwds):
    def wrapper(*args, **kwds):
        result = None
        exception_flag = False
        exception = None
        Var.ocrimg = None
        start_time = time.time()
        Var.case_snapshot_index += 1
        snapshot_index = Var.case_snapshot_index
        imagename = "Step_{}.png".format(snapshot_index)
        file = os.path.join(Var.snapshot_dir, imagename)
        action_step = args[-1]
        try:
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
        except Exception as e:
            exception = e
            exception_flag = True
        finally:
            try:
                if Var.ocrimg is not None:
                    cv2.imwrite(file, Var.ocrimg)
                    Var.ocrimg = None
                else:
                    Var.instance.save_screenshot(file)
                stop_time = time.time()
                duration = str('%.1f' % (stop_time - start_time))
                result_step = '{}|:|{}|:|{}s|:|{}|:|{}\n'.format(snapshot_index, not exception_flag, duration, imagename, action_step)
                with open(os.path.join(Var.snapshot_dir, 'result.log'), 'a') as f:
                    f.write(result_step)
            except:
                log_error(traceback.format_exc(), False)
            if exception_flag:
                raise exception
        return result
    return wrapper