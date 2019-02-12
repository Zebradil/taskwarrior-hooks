#!/usr/bin/env python3

import os
import subprocess
import sys

TASK_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

c = {}
if len(sys.argv) > 1:
    c = {k: v for k, v in (s.split(":", 1) for s in sys.argv[1:])}

if "args" not in c:
    c["args"] = "Taskwarrior version too old, no info available."

os.chdir(TASK_DIR)

if subprocess.call("git diff --exit-code --quiet".split()) != 0:
    subprocess.call("git commit -a".split() + ["-m" + c["args"]])

