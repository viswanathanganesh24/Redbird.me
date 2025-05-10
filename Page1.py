from PyQt5 import QtWidgets, uic
import sys, os
import csv
import pickle

# Important variable: used to tell program which account the user is logged into
user = None

widget = QtWidgets.QStackedWidget()

# Finding password (for use in login function)
def findpass(name):
    with open("userdata.csv", "r") as data:
        x = csv.reader(data)
        for i in x:
            if i[0] == name:
                return i[1]


# Getting list of usernames for easy access
existingUsernames = []


def quickinfo():
    with open("userdata.csv", "a+") as data:
        data.seek(0)
        x = csv.reader(data)
        for i in x:
            global existingUsernames
            existingUsernames += [i[0]]


quickinfo()


# Creating register function, no parameters, void
def register():
    class Ui(QtWidgets.QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('register.ui', self)

            self.username = self.findChild(QtWidgets.QLineEdit, 'username')
            self.username.setPlaceholderText("Please enter your username")

            self.password = self.findChild(QtWidgets.QLineEdit, 'password')
            self.password.setPlaceholderText("Please enter your password")

            self.regie = self.findChild(QtWidgets.QPushButton, 'regie')

            self.show()

            self.username.returnPressed.connect(lambda: rusername())
            self.password.returnPressed.connect(lambda: rpassword())


            def regie():
                rmsg = QtWidgets.QMessageBox()
                if fail1 == False and fail2 == False:
                    with open("userdata.csv", "a", newline="") as data:
                        w = csv.writer(data)
                        w.writerow([self.username.text(), self.password.text()])
                    rmsg.setText("Successfully registered! Please login now")

                    with open("friendslist.dat", "ab") as friendslist:  # Adding user to friendslist.dat
                        d = {'username': self.username.text(), 'friends': [], 'requests': []}
                        pickle.dump(d, friendslist)

                    with open("userdata.csv", "r") as data:
                        x = csv.reader(data)
                        for i in x:
                            global existingUsernames
                            existingUsernames += [i[0]]

                    rmsg.exec_()


            def rusername():
                global fail1
                fail1 = False
                umsg = QtWidgets.QMessageBox()
                if self.username.text() in existingUsernames:
                    umsg.setText('Username already exists. Please log in or retry.')
                    umsg.exec_()
                    fail1 = True
                else:
                    for i in self.username.text():
                        if i in "/[`!@#$%^&*()_+\-=\[\];':\"\\|,.<>\/?~]/":
                            umsg.setText('Username cannot contain special characters. Please retry.')
                            umsg.exec_()
                            fail1 = True
                        elif i.isspace():
                            umsg.setText('Username cannot have any spaces. Please retry.')
                            umsg.exec_()
                            fail1 = True


            def rpassword():  # Accepting valid password
                global fail2
                fail2 = False
                pmsg = QtWidgets.QMessageBox()
                if len(self.password.text()) < 8:
                    pmsg.setText('Password must contain more than 8 letters. Please retry.')
                    pmsg.exec_()
                    fail2 = True
                elif "," in self.password.text() or " " in self.password.text():
                    pmsg.setText('Password cannot contain comma or space. Please retry.')
                    pmsg.exec_()
                    fail2 = True
                else:
                    self.regie.clicked.connect(regie)


            app = QtWidgets.QApplication(sys.argv)
            window = Ui()
            app.exec_()


# Creating login function, no parameters, void
def login():
    class Ui(QtWidgets.QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('login.ui', self)

            self.username = self.findChild(QtWidgets.QLineEdit, 'username')
            self.username.setPlaceholderText("Please enter your username")

            self.password = self.findChild(QtWidgets.QLineEdit, 'password')
            self.password.setPlaceholderText("Please enter your password")

            self.login = self.findChild(QtWidgets.QPushButton, 'loginButton')

            self.show()

            self.username.returnPressed.connect(lambda: lusername())
            self.password.returnPressed.connect(lambda: lpassword())

            def lusername():
                global fail3
                fail3 = False
                umsg = QtWidgets.QMessageBox()
                if self.username.text() not in existingUsernames:
                    umsg.setText("Username not found. Please try again")
                    umsg.exec_()
                    fail3 = True


            def lpassword():
                global r
                r = False
                global fail4
                fail4 = False
                pmsg = QtWidgets.QMessageBox()
                check = findpass(self.username.text())
                if self.password.text() == check:
                    global user
                    user = self.username.text()
                    r = True
                    with open('user.txt', 'w') as f:
                        f.write(user)
                    self.login.clicked.connect(friends)
                else:
                    pmsg.setText("Wrong password, please try again.")
                    pmsg.exec_()
                    fail4 = True

                # Opening the mainpage


            def friends():
                class Ui(QtWidgets.QMainWindow):
                    def __init__(self):
                        super(Ui, self).__init__()
                        uic.loadUi('friends.ui', self)

                        with open("friendslist.dat", "rb") as friendList:
                            try:
                                while True:
                                    data = pickle.load(friendList)
                                    if data["username"] == user:
                                        self.friendcount=self.findChild(QtWidgets.QTextBrowser, 'friendcount')
                                    p = 'Friends: ' + str(len(data["friends"]))
                                    self.friendcount.setText(p)

                                    s = ''

                                    for i in data["friends"]:
                                        s = s + i + '\n'

                                    self.friend = self.findChild(QtWidgets.QTextBrowser, "friendlist")
                                    self.friend.setText(s)

                            except EOFError:
                                pass

                    self.requests = self.findChild(QtWidgets.QPushButton, 'requests')
                    self.chat = self.findChild(QtWidgets.QPushButton, 'chat')
                    self.show()

                    self.requests.clicked.connect(self.gotorequests)
                    self.chat.clicked.connect(self.cmd)


                    def cmd(self):
                        os.system('start cmd /k "python main.py"')

                    def gotorequests(self):
                        screen2 = requests()
                        widget.addWidget(screen2)
                        widget.setCurrentIndex(widget.currentIndex() + 1)


                class requests(QtWidgets.QMainWindow):
                    def __init__(self):
                        super(requests, self).__init__()
                        uic.loadUi('requests.ui', self)

                        self.acceptU = self.findChild(QtWidgets.QLineEdit, 'acceptU')
                        self.acceptU.setPlaceholderText("Please select user")

                        self.sendU = self.findChild(QtWidgets.QLineEdit, 'sendU')
                        self.sendU.setPlaceholderText("Enter username to send request to")

                        self.show()

                        self.acceptU.returnPressed.connect(lambda: acceptRequest())
                        self.sendU.returnPressed.connect(lambda: sendRequest())

                        with open("friendslist.dat", "rb") as friendList:
                            try:
                                while True:
                                    data = pickle.load(friendList)
                                    if data["username"] == user:
                                        self.requestcount = self.findChild(QtWidgets.QTextBrowser, 'requestcount')
                                        p = 'Requests: ' + str(len(data["requests"]))
                                        self.requestcount.setText(p)

                                        s = ''
                                        for i in range(len(data["requests"])):
                                            s = s + str(i) + ": " + data["requests"][i] + '\n'

                                        self.request = self.findChild(QtWidgets.QTextBrowser, "requestlist")
                                        self.request.setText(s)

                            except EOFError:
                                pass


                        # Function acceptRequest(username) allows user to accept a friend request
                        def acceptRequest():
                            accmsg = QtWidgets.QMessageBox()

                            try:  # Selecting the friend who's request is accepted
                                with open('friendslist.dat', 'rb') as friendslist:
                                    selectedBool = False
                                    while selectedBool == False:
                                        x = pickle.load(friendslist)
                                        if x["username"] == user:
                                            requests = x["requests"]

                                            if len(requests) > 0:
                                                while True:
                                                    if self.acceptU.text().isnumeric() and int(self.acceptU.text()) < len(requests):
                                                        selectedFriend = requests[int(self.acceptU.text())]
                                                        break
                                                    else:
                                                        accmsg.setText('Incorrect input, please retry')
                                                        accmsg.exec_()
                                                selectedBool = True
                                            elif len(requests) == 0:
                                                accmsg.setText('You have no requests to accept.')
                                                accmsg.exec_()
                                                break
                            except:
                                pass
                            if selectedBool == True:  # Changing friendslist to reflect new changes
                                try:
                                    with open('friendslist.dat', 'rb') as friendslist:
                                        with open('temp.dat', 'wb') as temp:
                                            while True:
                                                x = pickle.load(friendslist)
                                                if x["username"] == user:
                                                    x["requests"].remove(selectedFriend)
                                                elif x["username"] == selectedFriend and user not in x["friends"]:
                                                    x["friends"].append(user)
                                                pickle.dump(x, temp)
                                except:
                                    pass
                                os.remove("friendslist.dat")
                                os.rename("temp.dat", "friendslist.dat")
                                accmsg.setText('Friend request accepted!')
                                accmsg.exec_()

                            # Function sendRequest(username) sends a request to another user


                        def sendRequest():
                            request = self.sendU.text()
                            senmsg = QtWidgets.QMessageBox()

                            if request in existingUsernames:
                                with open("friendslist.dat",
                                          "rb") as friendslist:  # Using a temporary file to save data to and then renaming it later
                                    with open("temp.dat", "wb") as temp:
                                        try:
                                            p = True
                                            while p == True:
                                                x = pickle.load(friendslist)
                                                if x["username"] == request:
                                                    if user in x["requests"]:
                                                        p = False
                                                        senmsg.setText('You have already sent a request!')
                                                        senmsg.exec_()
                                                elif x["username"] == user:
                                                    if request in x["friends"]:
                                                        p = False
                                                        senmsg.setText('You are already friends!')
                                                        senmsg.exec_()
                                        except:
                                            pass
                                        try:
                                            friendslist.seek(0)
                                            while True:
                                                x2 = pickle.load(friendslist)
                                                if x2['username'] == request and p == True:
                                                    x2["requests"].append(user)
                                                    senmsg.setText('Request successfully sent.')
                                                    senmsg.exec_()
                                                pickle.dump(x2, temp)
                                        except:
                                            pass

                                os.remove("friendslist.dat")
                                os.rename("temp.dat", "friendslist.dat")

                            else:
                                senmsg.setText('User does not exist.')
                                senmsg.exec_()


                        self.friends = self.findChild(QtWidgets.QPushButton, 'friends')
                        self.show()

                        self.friends.clicked.connect(self.gotofriends)


                        def gotofriends(self):
                            screen1 = Ui()
                            widget.addWidget(screen1)
                            widget.setCurrentIndex(widget.currentIndex() + 1)


                        app = QtWidgets.QApplication(sys.argv)
                        widget = QtWidgets.QStackedWidget()
                        screen1 = Ui()
                        widget.addWidget(screen1)
                        widget.setFixedHeight(500)
                        widget.setFixedWidth(800)
                        widget.show()

                        try:
                            sys.exit(app.exec_())
                        except:
                            pass

                        if len(self.username.text()) == 0 or len(self.password.text()) == 0:
                            pass

                        app = QtWidgets.QApplication(sys.argv)
                        window = Ui()
                        app.exec_()


# Connecting the register and login buttons to the respective methods
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('page1.ui', self)

        self.register = self.findChild(QtWidgets.QPushButton, 'register_button')
        self.register.clicked.connect(register)

        self.login = self.findChild(QtWidgets.QPushButton, 'login_button')
        self.login.clicked.connect(login)

        self.show()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
