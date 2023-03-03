# system module
import os
import time
import sys
import argparse
import zipfile
import logging
import pdb

# 3rd parth module
from PIL import Image
from img2pdf import convert

# capture module
import ebook.ebook as eb
import device.device as dev


def capture(ebook, swipe, duration):
    for p in range(1, ebook.last_page):
        print("working page information => [%s/%s]" % (p, ebook.last_page))
        ebook.capture(sleep=0.7)
        ebook.next_page(swipe, sleep=0.7, dur=duration)

def extract_capture_files(device, title):
    path = "d:\\capture\\book\\{title}".format(title=title)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    os.chdir(path)
    cmd = "adb shell \"find /storage/emulated/0/DCIM/Screenshots/ -name kyobo*\""
    capture_files = os.popen(cmd).read().strip().split("\n")
    [os.system("adb pull %s" % f) for f in capture_files]

def elapsed_time(fn):
    def func(*args, **kwargs):
        t1 = time.time()
        print("* Starting work: %s" % str(t1))
        fn(*args)
        t2 = time.time()
        print("* Work done: %s" % str(t2))
        print("* Elapsed time: %s" % str(t2 - t1)[:5])
    return func

@elapsed_time
def zip_files(title):
    path = "d:\\capture\\book\\%s" % title
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    os.chdir(path)
    curr_path = os.getcwd()
    zip_filename = "%s.zip" % title
    zip_file = zipfile.ZipFile(os.path.join(curr_path, zip_filename), "w")
    files = os.listdir(".")
    files.remove(zip_filename)

    for f in files:
        zip_file.write(f, compress_type=zipfile.ZIP_DEFLATED)

    zip_file.close()

@elapsed_time
def make_pdf(title):
    path = "d:\\capture\\book\\%s" % title
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    os.chdir(path)

    files = os.listdir(".")
    files = [f for f in files if f.endswith(".png")]
    files.sort()

    pdf = convert(files)
    with open(title + ".pdf", "wb") as f:
        f.write(pdf)

def main():
    # parse argument
    arg = argparse.ArgumentParser()
    arg.add_argument('-l', '--lib', type=str, required=True, choices=['Seoul', 'Kyobo'], help='library name')
    arg.add_argument('-d', '--device', type=str, required=True, choices=['GalaxyS10', 'GalaxyTabS3'], help='mobile device name')
    arg.add_argument('-t', '--title', type=str, required=True, help='ebook title')
    arg.add_argument('-p', '--pages', type=int, required=True, help='pages of ebook')
    arg.add_argument('-u', '--swipe-duration', type=int, required=True, help='duration of swipe (unit: ms)')
    arg.add_argument('-s', '--swipe', type=int, required=False, default=1, 
        choices=[sw.value for sw in dev.SWIPE_DIRECTION], help='direction of swipe. 1:RL, 2:LR, 3:TB, 4:BT')
    out = arg.parse_args()

    # set argument
    lib_name = out.lib
    device_name = out.device

    # create ebook, device
    device = dev.DeviceFactory.get(device_name)
    ebook = eb.EbookFactory.get(lib_name)
    ebook.title = out.title
    ebook.last_page = out.pages
    ebook.device = device
    swipe = out.swipe
    duration = out.swipe_duration

    # capture every pages
    # capture(ebook, swipe, duration)

    # extract pages to local
    extract_capture_files(device, ebook.title)

    # zip files
    zip_files(ebook.title)

    # make pdf file
    make_pdf(ebook.title)

if __name__ == "__main__":
    main()