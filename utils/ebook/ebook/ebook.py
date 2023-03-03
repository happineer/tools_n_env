import time

class EbookFactory:
    def __init__(self):
        pass

    def get(lib_name, device=None):
        eb = None
        if lib_name == "Seoul":
            eb = SeoulLibEbook(device)
        elif lib_name == "Kyobo":
            eb = KyoboLibEbook(device)
        else:
            print("Not support [%s] ebook" % lib_name)
        return eb


class Ebook:
    def __init__(self, device):
        self.title = ""
        self.last_page = 0
        self.device = device
    
    def capture(self, sleep=1):
        print("capture!")
        time.sleep(sleep)

    def next_page(self, swipe_direction, sleep=1):
        pass

class KyoboLibEbook(Ebook):
    def __init__(self, device):
        self.device = device

    def _click_capture_icon(self):
        x, y = self.device.get_capture_icon_location()
        self.device.tap(x, y)

    def _close_warning_popup(self):
        x, y = self.device.get_warning_popup_icon_location()
        self.device.tap(x, y)

    def next_page(self, swipe_direction, sleep=1, dur=1):
        self.device.swipe(swipe_direction, dur)
        time.sleep(sleep)

    def capture(self, sleep=1):
        self._click_capture_icon()
        time.sleep(sleep)

        self._close_warning_popup()
        time.sleep(sleep)


class SeoulLibEbook(Ebook):
    def __init__(self, device):
        self.device = device

    def next_page(self, swipe_direction, sleep=1):
        self.device.swipe(swipe_direction)
        time.sleep(sleep)

    def capture(self, sleep=1):
        self.device.screen_capture(self.title)
        time.sleep(sleep)
