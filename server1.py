import socket, threading, time, os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates a socket for the server

server.bind(("localhost", 9999))  # server is binded to this port

connection_list = []  # list of all connections and user info
address_list = []

print("server running")


# Server listens to the incoming requests to connect and accepts and adds it to the connection_list
def CONNECTOR():
    while True:
        server.listen()
        connection, address = server.accept()
        connection_list.append([connection, ["#1", "#2"], False, False])


# a thread for the connector
connector_thread = threading.Thread(target=CONNECTOR)
connector_thread.start()


# this is the function which is assigned for each and every connection
def RECEIVER(conn):
    try:
        p = 0
        while True:
            if p == 0:
                client_info = conn[0].recv(1024).decode('utf-8')
                if "::" in client_info:
                    conn[1] = client_info.split("::")
                    for i in connection_list:
                        if i[0] == conn[0]:
                            i = conn
                else:
                    conn[1] = [client_info]
                    for i in connection_list:
                        if i[0] == conn[0]:
                            i = conn

                print(conn[1])
                # its is a list where index 0 is user and index 1 is friend
                p = 1

            if conn[1][0][-8::] != "_display":
                msg = conn[0].recv(1024).decode('utf-8')
                print(msg)
                for i in connection_list:
                    if conn[1][0::] == i[1][-1::-1] and i[3] != True:
                        friend_display = i[1][0] + "_display"
                        for j in connection_list:
                            if j[1][0] == friend_display:
                                try:
                                    j[0].send(msg.encode("utf-8"))
                                except:
                                    pass

    except:
        print(conn[1][0], "Offline")
        flag = 0
        while flag < 2:
            for i in connection_list:
                if i[1][0] == conn[1][0] + "_display":
                    try:
                        i[0].send("Die".encode("utf-8"))
                    except:
                        connection_list.remove(i)
                        flag += 1
                        break
                elif i[1][0] == conn[1][0]:
                    connection_list.remove(i)
                    flag += 1
                    break


# threader is the function which runs as a thread itself and assigns threads for different connections and their respective displays
def THREADER():
    while True:
        for c in connection_list:
            if c[2] == False and c[3] == False:
                t = threading.Thread(target=RECEIVER, args=(c,))
                t.start()
                c[2] = True


# this function shows the active threads in the server
def threadcounter():
    while True:
        os.system("cls")
        print("Active Threads:", threading.active_count())
        for i in connection_list:
            print(i[1])

        time.sleep(1)  # refreshes for every 1 sec


# assigning threads to the threader and counter
threader_thread = threading.Thread(target=THREADER)
counter_thread = threading.Thread(target=threadcounter)

# starting threads
threader_thread.start()
counter_thread.start()
