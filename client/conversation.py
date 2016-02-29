# -*- coding: utf-8-*-
import logging

from client.modules.CustomModule import getServerInstance
from notifier import Notifier
from brain import Brain


class Conversation(object):
    def __init__(self, persona, mic, profile):
        self._logger = logging.getLogger(__name__)
        self.persona = persona
        self.mic = mic
        self.profile = profile
        self.brain = Brain(mic, profile)
        self.notifier = Notifier(profile)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        try:
            actionSender = listenActions()
            while True:
                # Print notifications until empty
                notifications = self.notifier.getAllNotifications()
                for notif in notifications:
                    self._logger.info("Received notification: '%s'", str(notif))

                self._logger.debug("Started listening for keyword '%s'",
                                   self.persona)


                threshold, transcribed = self.mic.passiveListen(self.persona)
                self._logger.debug("Stopped listening for keyword '%s'",
                                   self.persona)


                if not transcribed or not threshold:
                    self._logger.info("Nothing has been said or transcribed.")
                    continue
                self._logger.info("Keyword '%s' has been said!", self.persona)

                self._logger.debug("Started to listen actively with threshold: %r",
                                   threshold)
                actionSender.activeListenTurnOn()
                input = self.mic.activeListenToAllOptions(threshold)
                self._logger.debug("Stopped to listen actively with threshold: %r",
                                   threshold)
                actionSender.activeListenTurnOff()
                if input:
                    self.brain.query(input)
                else:
                    self.mic.say(u"Не понятно")
        finally:
            server = getServer()
            if server is not None:
                server.close()


class listenActions:
    def __init__(self):
        self.server = getServer()

    def pushOnClient(self, id):
        if self.server is not None:
            self.server.send(self.generateJSON(id))

    def passiveListenTurnOn(self):
        print "passiveListenTurnOn"
        self.pushOnClient(-1)

    def passiveListenTurnOff(self):
        print "passiveListenTurnOff"
        self.pushOnClient(-2)

    def activeListenTurnOn(self):
        print "activeListenTurnOn"
        self.pushOnClient(-3)

    def activeListenTurnOff(self):
        print "activeListenTurnOff"
        self.pushOnClient(-4)

    @staticmethod
    def generateJSON(id):
        return {'key': id, 'args': []}


def getServer():
    server = getServerInstance()
    if server is None:
        print "Conversation bad server"
    return server
