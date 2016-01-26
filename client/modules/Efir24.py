## -*- coding: utf-8-*-
import datetime
import re
import subprocess
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["OPEN", "CLOSE", "TWENTY", "FOUR"]


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    global p, p_rtmpdump, p_omxplayer

    if bool(re.search(r'\bopen\stwenty\sfour\b', text, re.IGNORECASE)):
        mic.say("I am running Efir24 channel")

        cmd = ["sudo", "rm", "/tmp/efir24"]
        subprocess.call(cmd)

        cmd = ["mkfifo", "/tmp/efir24"]
        subprocess.call(cmd)

        cmd = ("rtmpdump -r rtmp://stream.efir24.tv:1935/live/efir24tv --live" +
               " -o /tmp/efir24 | omxplayer --vol 1000 -o local -b" +
               " --alpha 255 /tmp/efir24")
        # subprocess.call(cmd, shell=True)
        # p = subprocess.Popen(cmd, shell=True)

        cmd = ["rtmpdump", "-r", "rtmp://stream.efir24.tv:1935/live/efir24tv",
               "--live", "-o", "/tmp/efir24"]
        p_rtmpdump = subprocess.Popen(cmd)

        cmd = ["omxplayer", "--vol", "1000", "-o", "local", "-b", 
               "--alpha", "255", "/tmp/efir24"]
        p_omxplayer = subprocess.Popen(cmd)

    elif bool(re.search(r'\bclose\stwenty\sfour\b', text, re.IGNORECASE)):
	mic.say("I am closing Efir24 channel")

        p_omxplayer.terminate()
        p_rtmpdump.terminate()
    else:
        mic.say("I got that you want to do something with Efir24 channel, " +
                "but could you please say it more clear?")


def isValid(text):
    """
        Returns True if input is related to the Efir24 module.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bopen\stwenty\sfour\b|\bclose\stwenty\sfour\b', text, re.IGNORECASE))
