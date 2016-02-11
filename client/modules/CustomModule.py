# coding=utf-8
from server.Server import ServerSide

WORDS = [u"один", u"два", u"1"]


def handle(text, mic, profile):
    print u"IN HANDLE %s" % text
    pass


def isValid(text):
    print u"validate text %s" % text
    answer = None
    text = text.lower()
    for com in commandList:
        if com.checkOutput(text):
            answer = com.generateJSON()
            break  # TODO 09.02.16 what if several variants
    if answer is not None:
        server = getServerInstance()
        server.send(answer)
        return True
    else:
        return False


class Command:
    def __init__(self, words, args, identifier):
        self.words = words  # type: list
        self.args = args  # type: list
        self.id = identifier  # type: int

    def checkOutput(self, text):
        return Command._checkInCollection_(self.words, text) and Command._checkInCollection_(self.args, text)

    @staticmethod
    def _checkInCollection_(collection, text):
        if len(collection) == 0:
            return True
        for k in collection:
            if k in text:
                print u"word %s in %s" % (k, text)
                return True
        return False

    def generateJSON(self):
        return {'key': self.id}


# TODO 09.02.16 commands
commandList = [Command([u'позвони'], [u'мансуру', u'асхату', u'феде'], 1),
               Command([u'набери'], [u'мансура', u'асхата', u'федю'], 2),
               Command([u'алло', u'принять', u'принять звонок', u'принять входящий', u'принять входящий звонок',
                        u'ответить', u'ответь', u''], [], 3),
               Command([u'отклонить', u'отклонить вызов', u'отколони вызов',
                        u'положи трубку', u'положить трубку'], [], 4),
               Command([u'отбой', u'завершить', u'завершить вызов', u'клади трубку'], [], 5),
               Command([u'выключись', u'пора спать', u'отключение'], [], 6)]  # type: list[Command]


def getServerInstance():
    # server initialization
    # note: this work with reloading of module
    if 'server_key' in globals():
        print "Has been inited"
        print globals()['server_key']
    else:
        print 'init it'
        globals()['server_key'] = ServerSide()
    return globals()['server_key']


getServerInstance()
