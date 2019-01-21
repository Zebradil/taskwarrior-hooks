#!/usr/bin/env python

import os
import subprocess
import sys

TASK_DIR = os.path.dirname(__file__) + os.sep + os.pardir

c = {}
if len(sys.argv) > 1:
    c = {k: v for k, v in (s.split(":", 1) for s in sys.argv[1:])}

if "args" not in c:
    c["args"] = "Taskwarrior version too old, no info available."

os.chdir(TASK_DIR)

if not os.path.isdir(TASK_DIR + os.sep + ".git"):
    subprocess.call("git init".split())
    with open(".gitignore", "w") as f:
        f.write("*\n")
    subprocess.call("git add -f .gitignore pending.data completed.data".split())
    subprocess.call(["git", "commit", "-mInitial log"])

if subprocess.call("git diff --exit-code --quiet".split()) != 0:
    subprocess.call("git commit -a".split() + ["-m" + c["args"]])

