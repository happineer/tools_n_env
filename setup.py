#!/usr/bin/python

import os
import os.path
import pdb

curr_dir = os.getcwd()
home = os.getenv("HOME")

my_tools_dir = os.path.join(home, ".local/my_tools")
if os.path.exists(my_tools_dir):
    print(f"{my_tools_dir} is already exists")
    res = input("continue to run? [y/n] >> ")
    res = res.strip()
    if res != "y":
        print("Program is exit")
        exit(0)

os.system(f"mkdir -p {my_tools_dir}")

utils_dir = os.path.join(curr_dir, "utils")
files = next(os.walk(utils_dir), (None, None, []))[2]  # [] if no file
for f in files:
    print("[my_tools] put several util files under the .local/my_tools/")
    os.system(f"cp {utils_dir}/{f} {my_tools_dir}")


bashrc = os.path.join(home, ".bashrc")
with open(f"{bashrc}") as f:
    content = f.read()
    if not ".my_alias.rc" in content:
        print("[my_tools] add .my_alias.rc into .bashrc")
        os.system(f"echo \"source $HOME/.local/my_tools/.my_alias.rc\" >> {bashrc}")
