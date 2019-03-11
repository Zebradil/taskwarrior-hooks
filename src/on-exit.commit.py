#!/usr/bin/env python3

import datetime
import os
import subprocess
import sys

UPDATE_TIMEOUT = datetime.timedelta(hours=1)
TASK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
LAST_UPDATE_FILE = os.path.join(TASK_DIR, "_repo_updated_at")
NO_COMMIT_ENV = "TW_NO_COMMIT"

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
    if not os.getenv(NO_COMMIT_ENV):
        subprocess.call("git commit -a".split() + ["-m" + c["args"]])
    else:
        print(NO_COMMIT_ENV, " is set, no changes committed")


def r(cmd: str) -> str:
    return subprocess.run(cmd.split(), stdout=subprocess.PIPE).stdout.decode().strip()


requires_update = True
try:
    with open(LAST_UPDATE_FILE, "r") as f:
        last_update = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(int(f.read()))
        if last_update > UPDATE_TIMEOUT:
            print(f"Last update happend {last_update} ago")
        else:
            requires_update = False
except Exception as e:
    print(e)

if requires_update:
    subprocess.call("git remote update".split())
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(str(int(datetime.datetime.utcnow().timestamp())))

local = r(r"git rev-parse @")
remote = r(r"git rev-parse @{u}")
base = r(r"git merge-base @ @{u}")

if local == remote:
    pass  # Up-to-date
elif local == base:
    print("Need to pull")
    subprocess.call("git pull".split())
elif remote == base:
    print(f"There are not published changes. Run 'cd {TASK_DIR}; git push'")
else:
    print("Something wrong, please inspect the repo")
