# Import socket module
import socket
from _thread import start_new_thread
import time
import select
import sys
import os

# GLOBALS --------------------------------

host = 'localhost'                   # local host IP '127.0.0.1' or replace w/ external machine's ip address
port = 6030                          # Define the port on which you want to connect
MESSAGE_MAX_LENGTH_BYTES = 800       # max length of message body in bytes
disallowed_chars = ['%', '|', ' ']   # disallowed characters (used in packet encoding)
log_out = False                      # instigates an automatic log out when the user attempts to access the wrong account 

# colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# FUNCTIONS --------------------------------

def printb(msg):
    '''prints menu messages for the client in blue '''
    print(bcolors.OKBLUE + msg + bcolors.ENDC)

def get_username():
    '''Get username from user, ensuring it is valid.'''
    valid = False
    while valid is False:
        valid = True
        username = input()
        for char in disallowed_chars:
            if char in username:
                printb(f'Username "{username}" is invalid (must not contain "{char}"), please try again.')
                valid = False
                break
        
        if (len(username) > 20):
            printb(f'Username must not be longer than 20 characters, please try again.')
            valid = False

    return username

def get_message():
    '''Get message from user, ensuring it is valid.'''
    valid = False
    while valid is False:
        message = input()
        if (message == ''):
            print(f'Message must not be empty, please try again.')
        elif (len(message.encode('ascii')) > MESSAGE_MAX_LENGTH_BYTES):
            print(f'Message must not be longer than {MESSAGE_MAX_LENGTH_BYTES} bytes, please try again.')
        elif '%' in message:
            print('Message must not contain the character "%", please try again.')
        else:
            valid = True
    return message


# thread function
def threaded_receive(conn):
    global log_out
    '''Thread function for receiving messages from server.'''
    while True:
        # data received from client
        try:
            ready = select.select([conn], [], [], 1)
            if ready[0]:
                data = conn.recv(1024)
                # print('Data (raw):', data, ' len:', len(data))

                data = data.decode('ascii')
                # print('Data (decoded):', data, ' len:', len(data))

                if not data:
                    printb('Goodbye!')
                    break
                elif "SERVER%Kill" in data: 
                    # Server has sent a signal to kill the client because of an invalid request 
                    # (i.e. logging into an account which doesnt exist)
                    print(data.replace("SERVER%Kill", "").replace("|", ""))
                    log_out = True
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                    os._exit(1)

                # split incoming message into distict packets (delimited by '|')
                packets = data.split('|')
                for packet in packets:
                    if packet == '':
                        continue
                    sender, message = packet.split('%')
                    print(f"[{sender}] {message}")
        except Exception as e:
            # Error occurs when parent thread closes connection:
            #   not a problem as we are logging out anyway, so ignore
            break


def welcome_menu(client):
    '''Welcome menu for new users.'''
    print(bcolors.OKBLUE + '''
 __     __     ______     __         ______     ______     __    __     ______    
/\ \  _ \ \   /\  ___\   /\ \       /\  ___\   /\  __ \   /\ "-./  \   /\  ___\   
\ \ \/ ".\ \  \ \  __\   \ \ \____  \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  __\   
 \ \__/".~\_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ 
  \/_/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ 
                                                                                  
''' + bcolors.ENDC)
    printb('Hello! Type 0 to create an account, type 1 to log in.')

    valid = False
    while valid is False:
        response = input().replace(" ", "")
        if response == '0' :
            # create account or login (same effect)
            printb('Please enter your username.')
            client.create_account(get_username())
            valid = True

        elif response == '1':
            printb('Please enter your username.')
            client.login(get_username())
            valid = True

        else:
            printb('Invalid input. Please try again.')


class Client:

    def __init__(self, host, port):
        '''Initialize client.'''
        self.host = host
        self.port = port
        self.username = ''
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))

    def create_account(self, username):
        '''Create new account.'''
        self.username = username
        self.send_message('0', username)

    def login(self, username):
        '''Log in to existing account by sending message to server with opcode 1.'''
        self.username = username
        # TODO: handle failure
        self.send_message('1', username)

    def send_message(self, opcode, username, message=None, target=None, doTime=False):
        '''Send message to server with opcode, username, message, and target.'''
        start = time.time()
        msg = f'{opcode}%{username}%{target}%{message}'
        bmsg = msg.encode('ascii')
        self.conn.sendall(bmsg)
        end = time.time()
        if doTime:
            print("timing: ", end - start)
            print("size of: ", sys.getsizeof(bmsg))
        # printb(f'Message sent.')

    def query_message(self):
        '''Obtain message details from user and send to server.'''
        printb('Please enter username of recipient.')
        target = get_username()
        printb('Please enter your message.')
        message = get_message()
        self.send_message(2, self.username, message, target)

    def logout(self):
        '''Log out of account by closing connection to server.'''
        self.send_message('3', self.username)
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()
        printb('You are logged out. Exiting ...')

    def list_all_users(self):
        '''
        Request a list of all users from the server.
        Server will respond with a list of all users, which will be printed to the console.
        '''
        self.send_message('5', self.username)

def Main():
    '''Main messaging loop.'''
    global log_out
    # create new client instance
    client = Client(host, port)

    # start thread for receiving messages in background
    start_new_thread(threaded_receive, (client.conn,))

    # log in / create account
    welcome_menu(client)

    try:

        while True:
            # sleep for a moment to improve user experience
            time.sleep(0.5)
            
            if log_out:
                exit()

            # show menu to user
            printb('Select an option: \n2 to send message, 3 to log out, 4 to delete account, 5 to list all online users.')

            # strip whitespace from input
            op = input().replace(" ", "")

            # take action based on user input
            if op == "2":
                # send message
                client.query_message()
            elif op == "3":
                # logout
                client.logout()
                exit()
            elif op == "4":
                # delete account
                client.send_message('4', client.username)
                client.logout()
                exit()
            elif op == "5":
                # list all users
                client.list_all_users()
            else:
                print('Invalid input. Please try again.')

    except KeyboardInterrupt as e:
        # Ensure client is properly logged out if user presses Ctrl+C
        client.logout()
        time.sleep(1)
        exit()


if __name__ == '__main__':
    Main()
