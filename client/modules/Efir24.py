## -*- coding: utf-8-*-
import datetime
import re
import subprocess
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["TWENTY", "FOUR"]


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

#    cmd = "sudo rm /tmp/efir24"
#    subprocess.call(cmd)

    cmd = "mkfifo /tmp/efir24"
    subprocess.call(cmd)

    cmd = ("rtmpdump -r rtmp://stream.efir24.tv:1935/live/efir24tv --live" +
           " -o /tmp/efir24 | omxplayer --vol 1000 -o local -b --alpha 255" +
           " /tmp/efir24")
    subprocess.call(cmd)

def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\btwenty four\b', text, re.IGNORECASE))
