import subprocess as sp
import requests
from utils.util import wait
from utils.log import debug, info, error

def isRunning():
    out = sp.check_output(r'schtasks.exe /query /tn "shuffleIP"', shell=True)
    if "Ready" in str(out):
        return False
    elif "Running" in str(out):
        return True
    else:
        raise Exception("Unknown state of task")

def internetAccess():
    timeout = 1
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def shuffle():
    # TEMP
    # info("Skipping IP shuffle")
    # return
    debug("Shuffling IP")
    task_name = "shuffleIP"
    command = ["schtasks", "/run", "/tn", task_name]
    sp.run(command)

    while isRunning():
        wait(2)
    
    wait(4)
    
    if not internetAccess():
        raise Exception("No internet access after shuffling IP")
    