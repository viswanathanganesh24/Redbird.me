import socket


def Client(username, friendname, chatfile):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates a socket for the client to connect to
    try:
        client.connect(("localhost", 9999))  # connects to the server port
    except:
        print("Live Chat is offline! [ClientError]")  # if the server isnt up then prints the following

    client_info = username + "::" + friendname  # the first msg is the username and the friendname

    try:
        client.send(client_info.encode("utf-8"))  # trying to send the username
    except:
        pass

    while True:  # infinite loop to get user input i.e., the msgs
        prompt = username + " : "  # prompt for decoration
        msg = input(prompt)
        if msg != "":  # validation for null string
            msg1 = prompt + msg
            with open(chatfile, 'a') as f:
                f.write(msg1 + "\n")
            try:
                client.send(msg1.encode("utf-8"))  # trying to send msg to the server
            except:
                pass
        else:
            print("\033[F", end='')  # ansi sequence for command editing


def Display(username):
    displayName = username + "_display"  # format of display name
    display = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket for display

    try:
        display.connect(("localhost", 9999))  # tries to connect to the server
    except:
        print("Server is offline! [DisplayError]")
        return 0  # ends the display

    display.send(displayName.encode('utf-8'))  # sends its name

    while True:
        received = display.recv(1024).decode('utf-8')  # always recieves msg from server
        print("\r", received + " " * 80 + "\n" + username + " : ", sep="", end="")  # command editing and printing
