from JSONSocket import Client, Server
#
# # Client code:
print "init"
client = Client()
print "connect & send"
client.connect('127.0.0.1', 27555).send({'some_list': [123, 456]})
print "receive"
while True:
    response = client.recv()
    print response
client.close()