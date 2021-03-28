#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import platform


class DevicesUtils(object):

    def __init__(self, platformName, udid):
        self._platformName = platformName
        self._udid = udid

    def device_info(self):

        if self._platformName.lower() == 'android':
            devices = self.get_devices()
            if self._udid and (self._udid not in devices):
                raise Exception("device {} not found!".format(self._udid))
            elif not self._udid and devices:
                self._udid = devices[0]
            elif not self._udid:
                raise Exception("Can‘t find device!")

            if platform.system() == "Windows":
                pipe = os.popen("adb -s {} shell getprop | findstr product".format(self._udid))
            else:
                pipe = os.popen("adb -s {} shell getprop | grep product".format(self._udid))
            result = pipe.read()
            manufacturer = "None" if not result else \
                re.search(r"\[ro.product.manufacturer\]:\s*\[(.[^\]]*)\]", result).groups()[0]
            model = "None" if not result else \
                re.search(r"\[ro.product.model\]:\s*\[(.[^\]]*)\]", result).groups()[0].split()[-1]
            device_type = "{}_{}".format(manufacturer, model).replace(" ", "_")
        elif self._platformName.lower() == 'ios':
            devices = self.get_devices('idevice_id -l')
            simulator_devices = self.get_devices('instruments -s Devices')
            if self._udid and (self._udid not in (devices or simulator_devices)):
                raise Exception("device {} not found!".format(self._udid))
            elif not self._udid and devices:
                self._udid = devices[0]
            elif not self._udid:
                raise Exception("Can‘t find device!")

            if self._udid in devices:
                DeviceName = os.popen('ideviceinfo -u {} -k DeviceName'.format(self._udid)).read()
                if not DeviceName:
                    DeviceName = 'iOS'
                device_type = DeviceName.replace(' ', '_')
            else:
                device_type = self._platformName
        else:
            raise  Exception("Test Platform must be Android or iOS!")

        return self._udid,device_type

    def get_devices(self,cmd=''):
        if self._platformName.lower() == 'android':
            pipe = os.popen("adb devices")
            deviceinfo = pipe.read()
            devices = deviceinfo.replace('\tdevice', "").split('\n')
            devices.pop(0)
            while "" in devices:
                devices.remove("")
        else:
            pipe = os.popen(cmd)
            deviceinfo = pipe.read()
            r = re.compile(r'\[(.*?)\]', re.S)
            devices = re.findall(r, deviceinfo)
            devices = devices if devices else deviceinfo.split('\n')
            while "" in devices:
                devices.remove("")

        return devices
