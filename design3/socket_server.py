import socket
from _thread import start_new_thread
import threading
from socket_client import bcolors

# GLOBALS --------------------------------

sessions = dict()       # who is logged in (usernames: connection | None)
messages = dict()       # stores who has outstanding messages
HOST = "localhost"      # open to broader network to connect across machines
PORT = 6030

server_lock = threading.Lock()

# FUNCTIONS --------------------------------

def printg(msg):
    '''prints menu messages for the client in blue '''
    print(bcolors.OKGREEN + msg + bcolors.ENDC)

def create_account(username, connection):
    # connection of all logged in users stored in sessions upon log in or, equivalently, account creation
    sessions[username] = connection
    printg(f"> {username} has created an account.")

def login(username, connection):
    # user added to the active list (sessions)
    sessions[username] = connection
    printg(f"> {username} has logged in.")

def logout(username):
    # connection information removed upon log out
    sessions[username] = None
    printg(f"> {username} has logged out.")

def queue_message(sender, recipient, message):
    # messages queued if the intended recipient is not currently logged in
    if recipient not in messages:
        messages[recipient] = []
    messages[recipient].append((sender, message))

def send_pending(messages, username):
    '''
    sends outstanding messages to the client who has just queried the server
    applies for a backlog of messages (seen upon log in) and real time messages (seen while logged in)
    '''
    if username in messages:
        info_msg = f"You have {len(messages[username])} new messages since you last logged in:"
        to_client(username, info_msg)

        for sender, message in messages[username]:
            to_client(username, message, sender)
        messages.pop(username)

def to_client(recipient, message, sender="SERVER", conn=None):
    data = f"{sender}%{message}|"
    print('Sending to', recipient, ':', data)

    if conn is not None:
        conn.sendall(data.encode('ascii'))
    else:
        sessions[recipient].sendall(data.encode('ascii'))

# thread function
def threaded(c):
    while True:
        # data received from client
        data = c.recv(1024)
        with server_lock:

            # a thread has dropped, likely indicating that a user has logged out or deleted their account
            if not data:
                printg('> HOMIE DEPARTURE ALERT')
                break

            data = data.decode('ascii')
            print(f"The data is: {data}")

            opcode, username, target, message = data.split('%')
            # print(opcode, username, target, message)

            # CREATE ACCOUNT
            if opcode == '0':
                if username in sessions:
                    # if user already exists, log in
                    if sessions[username] is not None:
                        # someone else is logged into the requested account
                        toClient = "KillSomeone else has logged into this account so you're being logged out. Goodbye!"
                        logout(username)
                    login(username, c)
                    to_client(username, f"User already exists. Welcome back, {username}.\n")
                else:
                    # user does not exist yet, create new user and log in
                    create_account(username, c)
                    to_client(username, f"Welcome to your new account, {username}.\n")

            # LOG IN
            elif opcode == '1': # log in
                if username not in sessions:
                    # user does not exist, give error
                    to_client(username, "KillAccount does not exist. Please create an account first.", conn=c)
                    break

                if sessions[username] is not None:
                    # someone else is logged into the requested account
                    to_client(username, "KillSomeone else has logged into this account so you're being logged out. Goodbye!")
                    logout(username)

                login(username, c)
                to_client(username, f"Welcome back, {username}")
                # Send undelivered messages, if any
                send_pending(messages, username)

            # SEND MESSAGE
            elif opcode == '2':
                if target not in sessions.keys():
                    # TODO: raise exception instead?
                    to_client(username, f"Error: User {target} does not exist. Message could not be sent")
                else:
                    if sessions[target] == None:
                        # target is not logged in, queue message
                        queue_message(username, target, message)
                    else:
                        # send message to target
                        printg(f"> {username} is trying to send a message to {target}.")
                        to_client(target, message, username)

            # LOG OUT
            elif opcode == '3':
                logout(username)

            # DELETE ACCOUNT
            elif opcode == '4':
                to_client(username, "Your account has been deleted. Goodbye!")
                sessions.pop(username)
                if username in messages:
                    messages.pop(username)

            # LIST ALL USERS
            elif opcode == '5':
                # Return a list of all users who are currently logged in
                to_client(username, str([key for key in sessions.keys() if sessions[key] is not None and sessions[key].fileno() != -1]), "ALL ACCOUNTS")


    # connection closed
    c.close()


class Server:

    def __init__(self, testing=False):
        self.testing = testing

    def start(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        print("Socket binded to port", port)

        # put the socket into listening mode
        self.socket.listen(5)
        print("Socket is listening!")

        # a forever loop until client wants to exit
        while True:

            try:
                # establish connection with client
                c, addr = self.socket.accept()
            except ConnectionAbortedError as e:
                if self.testing:
                    print("Connection aborted")
                    break
                else:
                    raise e

            # lock acquired by client
            # print_lock.acquire()
            printg("-------------------")
            printg("> NEW HOMIE ALERT")
            printg('> Connected to :' + str(addr[0]) + ':' + str(addr[1]))

            # Start a new thread and return its identifier
            start_new_thread(threaded, (c,))

        self.socket.close()

    def stop(self):
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    server.start(HOST, PORT)
