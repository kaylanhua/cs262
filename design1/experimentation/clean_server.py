# import socket programming library
import socket

# import thread module
from _thread import start_new_thread
import threading

sessions = dict()  # who is logged in (usernames: connection | None)
messages = dict()
HOST = "0.0.0.0"
PORT = 6023

# print_lock = threading.Lock()

# TODO: locking 

def create_account(username, connection):
    sessions[username] = connection
    print(f"{username} has created an account")
        
def login(username, connection):
    sessions[username] = connection
    print(f"{username} has logged in")
    
def logout(username):
    sessions[username] = None
    # self.socket.close()
    print(f"{username} has logged out")

def queue_message(sender, recipient, message):
    if recipient not in messages:
        messages[recipient] = []
    messages[recipient].append((sender, message))
        
def send_pending(messages, username):
    if username in messages:
        info_msg = f"You have {len(messages[username])} new messages since you last logged in:"
        to_client(username, info_msg)

        # TODO: reads may happen together

        for sender, message in messages[username]:
            to_client(username, message, sender)
        messages.pop(username)

def to_client(recipient, message, sender="SERVER"):
    data = f"{sender}%{message}|"
    print('sending to', recipient, ':', data)
    
    sessions[recipient].sendall(data.encode('ascii'))

# thread function
def threaded(c):
    while True:
        # data received from client
        data = c.recv(1024)
        print('Data (raw):', data, ' len:', len(data))
        
        if not data:
            print('HOMIE DEPARTURE ALERT')
            # lock released on exit
            # print_lock.release()
            break
        
        data = data.decode('ascii') 
        print(f"The data is: {data}")
        
        opcode, username, target, message = data.split('%')
        print(opcode, username, target, message)
        
        # CREATE ACCOUNT
        if opcode == '0':
            if username in sessions:
                # user alr exists, log in
                login(username, c)
                # TODO: raise exception, user already exists
            else:
                # user does not exist yet, create new user and log in
                create_account(username, c)
                to_client(username, f"Welcome to your new account, {username}")
        
        # LOG IN
        elif opcode == '1': # log in
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
                    print(f"someone is trying to send a message to {target}")
                    to_client(target, message, username)
        
        # LOG OUT            
        elif opcode == '3': 
            to_client(username, "You have logged out. Goodbye!")
            logout(username)

        # DELETE ACCOUNT    
        elif opcode == '4':
            to_client(username, "Your account has been deleted. Goodbye!")
            sessions.pop(username)
            if username in messages:
                messages.pop(username)
        
        # LIST ALL USERS    
        elif opcode == '5':
            to_client(username, str(list(sessions.keys())), "ALL ACCOUNTS")

    # connection closed
    c.close()


class Server:

    def __init__(self, testing=False):
        self.testing = testing

    def start(self, host, port):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        print("socket binded to port", port)

        # put the socket into listening mode
        self.socket.listen(5)
        print("socket is listening")

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
            print("-------------------")
            print("NEW HOMIE ALERT")
            print('Connected to :', addr[0], ':', addr[1])

            # Start a new thread and return its identifier
            start_new_thread(threaded, (c,))
        
        self.socket.close()

    def stop(self):
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    server.start(HOST, PORT)
