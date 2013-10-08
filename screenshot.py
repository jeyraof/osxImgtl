# -*- coding: utf-8 -*-

import config
import os
import sys
import subprocess
import time
import json
import requests


def main(param=0):
    if param is 0:
        intro()
        idx = int(raw_input("Which? : "))

    else:
        idx = param

    now = time.time()
    isFile = takeShot(idx, now)
    if isFile:
        result = upload(now)

        if result["status"] == "success":
            toClipboard(result["data"]["url"]["page"])
            print "[Success] " + result["data"]["url"]["page"]
        else:
            toClipboard("")
            print "[Error] upload Failed"
            print result

        removeShot(now)
    else:
        print "[Error] Canceled."
        return


def takeShot(idx, now):
    case = {
        1: "",
        2: "-iW",
        3: "-s"
    }
    command = "screencapture %s %s.png &> /dev/null" % (case[idx], now)
    subprocess.call(command, shell=True)

    if os.path.exists("%s.png" % now):
        return True
    else:
        return False


def removeShot(now):
    os.remove("%s.png" % now)


def upload(now):
    url = config.upload
    image = {'file': open("%s.png" % now, 'rb')}
    data = {'desc': config.desc}
    headers = {}
    if len(config.token) > 0:
        headers['X-IMGTL-TOKEN'] = config.token

    r = requests.post(url, data=data, files=image, headers=headers)
    return json.loads(r.text)


def toClipboard(string):
    command = 'echo %s | tr -d "\n" | pbcopy' % string
    subprocess.call(command, shell=True)


def intro():
    print "==========================="
    print "Screenshot upload to Img.tl"
    print "==========================="
    print "You can also use like bot. "
    print "$ python screenshot.py [#] "
    print "==========================="
    print "[1] Full Screen"
    print "[2] Select Window"
    print "[3] Draw Rectangular Form"
    print "==========================="

if __name__ == "__main__":
    if len(sys.argv) > 1:
        param = int(sys.argv[1])
        main(param)
    else:
        main()
