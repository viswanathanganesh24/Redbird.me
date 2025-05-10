import pickle, os

userFriends = None
chatFile = None
friend = None

# Refreshes friend data of user
def info(user):
    with open ('friendslist.dat','rb') as fList:
        global userFriends
        while True:
            details = pickle.load(fList)
            if details['username'] == user:
                global userInfo
                userFriends = details['friends']
                break

# Allows user to select friend to chat with
def chooseFriend(user):
    info(user)
    global userFriends, friend
    if len(userFriends) > 0:
        print("Your friends are:", userFriends)
        while True:     # Accept friend to chat with
            friend = input("Enter friend to chat with: ")
            if friend in userFriends:
                break
            else:
                print("Incorrect input, please retry \n")
    elif len(userFriends) == 0:
        print("You dont have any friends to chat with! For now, try messaging Admin dnfy")
        friend = "dnfy"


def findFile(user):
    global chatFile, friend

    chatName1 = 'chatdata\\' + user + '_' + friend
    chatName2 = 'chatdata\\' + friend + '_' + user
    if os.path.exists(chatName2):
        chatFile = chatName2
    else:
        chatFile = chatName1
        with open(chatFile, 'a') as f1:
            pass

def chatInitialiser():
    global chatFile
    os.system("cls")
    with open(chatFile) as FILE:
        DISPLAYCOUNT = 50
        LINES = FILE.readlines()
        if len(LINES) > DISPLAYCOUNT:
            print(''.join(LINES[-1 * DISPLAYCOUNT:]))
            print()
        else:
            print(''.join(LINES))
            print()

def chatp1(username):
    global userFriends, chatFile, friend
    chooseFriend(username)
    findFile(username)
    chatInitialiser()

    return friend, chatFile
