#!/usr/bin/env python3

import os
import subprocess
import sys

TASK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

os.chdir(TASK_DIR)

if subprocess.call("git rev-parse --quiet".split()) != 0:
    print(f"{TASK_DIR} is not a git repository, skip commiting changes")
    sys.exit(1)

c = {}
if len(sys.argv) > 1:
    c = {k: v for k, v in (s.split(":", 1) for s in sys.argv[1:])}

if "args" not in c:
    c["args"] = "Taskwarrior version too old, no info available."

if subprocess.call("git diff --exit-code --quiet".split()) != 0:
    subprocess.call("git commit -a".split() + ["-m" + c["args"]])

def r(cmd: str) -> str:
    return subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode().strip()

local = r(r"git rev-parse @")
remote = r(r"git rev-parse @{u}")
base = r(r"git merge-base @ @{u}")

if local != remote and remote == base:
    print(f"There are not published changes. Run 'cd {TASK_DIR}; git push'")
