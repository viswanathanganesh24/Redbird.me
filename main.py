import client1 as c, threading
from chat import *

def CHAT(username):
    friendname, file = chatp1(username)

    client_thread = threading.Thread(target=c.Client, args=(username, friendname, file))
    display_thread = threading.Thread(target=c.Display, args=(username,))
    client_thread.start()
    display_thread.start()

with open('user.txt','r') as f:
    user = f.read()
CHAT(user)
