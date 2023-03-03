import os
import time
import json
from enum import Enum

class SWIPE_DIRECTION(Enum):
    RIGHT_TO_LEFT = 1
    LEFT_TO_RIGHT = 2
    TOP_TO_BOTTOM = 3
    BOTTOM_TO_TOP = 4
    CUSTOM1 = 10

class DeviceFactory:
    def get(dev_name):
        dev = None
        if dev_name == "GalaxyS10":
            dev = GalaxyS10()
        elif dev_name == "GalaxyTabS3":
            dev = GalaxyTabS3()
        else:
            print("Not support [%s] device" % dev_name)
        return dev

class Device:
    def __init__(self):
        self.name = ""
        self.width = 0
        self.height = 0
        self.screenshot_path = ""

    def tap(self, x, y):
        cmd = "adb shell input tap {x} {y}".format(x=x, y=y)
        os.system(cmd)

    def screen_capture(self):
        print("screen_capture!")

    def get_capture_icon_location(self):
        print("[Error] this method should be implemented by child class")
        exit(-1)

    def get_warning_popup_icon_location(self):
        print("[Error] this method should be implemented by child class")
        exit(-1)

    def extract(self):
        cmd = "adb pull {path}/".format(path=self.screenshot_path)
        os.system(cmd)
    
class GalaxyTabS3(Device):
    def __init__(self):
        self.name = "GalaxyTabS3"
        conf_file = "./config/{dev}.json".format(dev=self.name)
        if not os.path.exists(conf_file):
            print("[Error] conf_file is not found : %s" % conf_file)
            exit(-1)
        self.dev_config = json.loads(open(conf_file).read())
        self.width = self.dev_config["width"]
        self.height = self.dev_config["height"]
        self.screenshot_path = self.dev_config["screenshot_path"]

    def _is_valid_x_location(self, x):
        return 0 < x < self.width 

    def _is_valid_y_location(self, y):
        return 0 < y < self.height

    def _swipe(self, x1, y1, x2, y2, dur):
        valid_x = all([self._is_valid_x_location(loc) for loc in (x1, x2)])
        if not valid_x:
            print("[Error] x1 or x2 not valid")
            exit(-1)

        valid_y = all([self._is_valid_y_location(loc) for loc in (y1, y2)])
        if not valid_y:
            print("[Error] y1 or y2 not valid")
            exit(-1)

        cmd = "adb shell input swipe {x1} {y1} {x2} {y2} {duration}".format(
            x1=x1, y1=y1, x2=x2, y2=y2, duration=dur
        )
        print("ADB command = %s" % cmd)
        os.system(cmd)

    def swipe(self, direction=SWIPE_DIRECTION.RIGHT_TO_LEFT, duration=200):
        swipe_params = self.dev_config["swipe"][str(direction)]
        swipe_params.append(duration)
        self._swipe(*tuple(swipe_params))

    def screen_capture(self, title):
        print("[GTab] screen_capture!")
        filename = "{t}_{time_ns}.png".format(
            t=title, time_ns=str(time.time_ns())[6:13]
        )
        cmd = "adb shell screencap -p {screenshot_path}/{f}".format(
            screenshot_path=self.screenshot_path, f=filename)
        print("[ADB Command]: ", cmd)
        os.system(cmd)

    def get_capture_icon_location(self):
        return (1450, 1780)

    def get_warning_popup_icon_location(self):
        return (780, 1170)



class GalaxyS10(Device):
    def __init__(self):
        self.name = "GalaxyS10"
        conf_file = "./config/{dev}.json".format(dev=self.name)
        if not os.path.exists(conf_file):
            print("[Error] conf_file is not found : %s" % conf_file)
            exit(-1)
        self.dev_config = json.loads(open(conf_file).read())
        self.width = self.dev_config["width"]
        self.height = self.dev_config["height"]
        self.screenshot_path = self.dev_config["screenshot_path"]
        self.swipe_params = None

    def _is_valid_x_location(self, x):
        return 0 < x < self.width 

    def _is_valid_y_location(self, y):
        return 0 < y < self.height

    def _swipe(self, x1, y1, x2, y2, dur):
        valid_x = all([self._is_valid_x_location(loc) for loc in (x1, x2)])
        if not valid_x:
            print("[Error] x1 or x2 not valid")
            exit(-1)

        valid_y = all([self._is_valid_y_location(loc) for loc in (y1, y2)])
        if not valid_y:
            print("[Error] y1 or y2 not valid")
            exit(-1)

        cmd = "adb shell input swipe {x1} {y1} {x2} {y2} {duration}".format(
            x1=x1, y1=y1, x2=x2, y2=y2, duration=dur
        )
        print("ADB command = %s" % cmd)
        os.system(cmd)

    def swipe(self, direction=SWIPE_DIRECTION.RIGHT_TO_LEFT, duration=1000):
        if not self.swipe_params:
            self.swipe_params = self.dev_config["swipe"][str(direction)]
            self.swipe_params.append(duration)
        self._swipe(*tuple(self.swipe_params))

    def screen_capture(self, title):
        print("[GS10] screen_capture!")
        filename = "{t}_{time_ns}.png".format(
            t=title, time_ns=str(time.time_ns())[6:13]
        )
        cmd = "adb shell screencap -p {screenshot_path}/{f}".format(
            screenshot_path=self.screenshot_path, f=filename)
        print("[ADB Command]: ", cmd)
        os.system(cmd)

    def get_capture_icon_location(self):
        return (1300, 2500)

    def get_warning_popup_icon_location(self):
        return (770, 1800)

