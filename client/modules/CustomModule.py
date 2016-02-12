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
        self.parsedArgs = []

    def checkOutput(self, text):
        self.parsedArgs = Command._getArgs_(self.args, text)
        return Command._checkInWordCollection_(self.words, text)

    @staticmethod
    def _checkInWordCollection_(collection, text):
        if len(collection) == 0:
            return True
        for word in collection:
            if word.lower() in text and word != u"":
                print u"word %s in %s" % (word, text)
                return True
        return False

    @staticmethod
    def _getArgs_(collection, text):
        text = text.lower()
        if len(collection) == 0:
            return []
        print u'collection %s' % collection[1]
        args = []
        synonyms = collection[0]

        checkedWords = []

        for index, synonymTuple in enumerate(synonyms):
            for word in synonymTuple:
                checkedWords.append(word.lower())
                if word.lower() in text and word != u'':
                    print u'append %s' % collection[1][index]
                    args.append(collection[1][index])
                    break
        print checkedWords
        return args

    def generateJSON(self):
        return {'key': self.id, 'args': self.parsedArgs}


# TODO 09.02.16 commands
commandList = [Command([u'позвони'], [[(u'мансуру', u'mansur', u'monster'), (u'асхату', u'асхат'), (u'феде', u'федя')],
                                      [u'mansur', u'asxat', u'fedya']], 1),
               Command([u'набери'],
                       [[(u'мансура',), (u'асхата', u'асхатов', u' асхат'), (u'федю', u'сейчас', u'хейзел', u'север')],
                        [u'mansur', u'asxat', u'fedya']], 1),
               Command([u'алло', u'принять', u'принять звонок', u'принять входящий', u'принять входящий звонок',
                        u'ответить', u'ответь', u''], [], 3),
               Command([u'отклонить', u'отклонить вызов', u'отколони вызов',
                        u'положи трубку', u'положить трубку'], [], 4),
               Command(
                   [u'отбой', u'завершить', u'завершить вызов', u'завершить вызов', u'решить вызов' u'клади трубку'],
                   [], 2)
               ]


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
