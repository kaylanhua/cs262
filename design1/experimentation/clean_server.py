# import socket programming library
import socket

# import thread module
from _thread import start_new_thread
import threading

sessions = dict()  # who is logged in (usernames: connection | None)
messages = dict()
HOST = "127.0.0.1"
PORT = 6022

# print_lock = threading.Lock()

def create_account(username, connection):
    print(f"{username} has created an account")
    login(username, connection)
        
def login(username, connection):
    sessions[username] = connection
    print(f"{username} has logged in")
    
def logout(username):
    sessions[username] = None
    # self.socket.close()
    print(f"{username} has logged out")

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
        
        status = 0 # not an error
        text = ''
        
        if opcode == '0':
            if username in sessions:
                # user alr exists, log in
                login(username, c)
            else:
                # user does not exist yet, create new user and log in
                create_account(username, c)
        elif opcode == '1': # log in
            login(username, c)
            
            # TODO: receive queue of msgs
            if username in messages:
                for message in messages[username]:
                    sessions[username].sendall(message.encode('ascii'))
                messages.pop(username)
        elif opcode == '2': # send message
            if target not in sessions.keys():
                # TODO: raise exception instead
                status = 1
                text = (f"User {target} does not exist")
            else: 
                toSend = username+'%'+message
                if sessions[target] == None: # target is not logged in
                    # user not logged in
                    if target not in messages:
                        messages[target] = []
                    messages[target].append(toSend)
                else:
                    # send message to target
                    print(f"someone is trying to send a message to {target}")
                    sessions[target].sendall(toSend.encode('ascii'))
                    # recipient = '1'
                    # arg1 = target
                    # arg2 = toSend
                    # send_message(1, target, toSend)
        elif opcode == '3': # log out
            logout(username)
            text = "You have logged out."
            # send_message(0, username, response)
        elif opcode == '4': # delete account
            sessions.pop(username)
            messages.pop(username)
            text = "Your account has been deleted."
        elif opcode == '5': # list all users
            text = str(list(sessions.keys()))
            text = 'all accounts' + '%' + text
            c.sendall(text.encode('ascii'))
            # send_message(0, username, message)

    # connection closed
    c.close()


def Main():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("socket binded to port", PORT)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        # print_lock.acquire()
        print("-------------------")
        print("NEW HOMIE ALERT")
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    
    s.close()


if __name__ == '__main__':
    Main()
