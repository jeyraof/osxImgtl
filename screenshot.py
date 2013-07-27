# -*- coding: utf-8 -*-

import config
import os
import subprocess
import time
import json
import requests


def main():
    print "==========================="
    print "Screenshot upload to Img.tl"
    print "==========================="
    print "[1] Full Screen"
    print "[2] Select Window"
    print "[3] Draw Rectangular Form"
    print "==========================="

    idx = int(raw_input("Which? : "))
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
    image = {'image': open("%s.png" % now, 'rb')}
    postdata = {'token': config.token, 'desc': config.desc}

    r = requests.post(url, data=postdata, files=image)
    return json.loads(r.text)


def toClipboard(string):
    command = 'echo %s | tr -d "\n" | pbcopy' % string
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    main()
