from __future__ import print_function

import logging
import grpc
import messages_pb2
import messages_pb2_grpc
import time
import sys
from _thread import start_new_thread

from socket_client import get_username, get_message, printb, bcolors

# GLOBALS --------------------------------

HOST = 'localhost'  # alternatively, use ip address of external server
# PORT = '50051'
# PORTS = [PORT, PORT+1, PORT+2]

PORT = 6740
PORTS = {'A': PORT, 'B': PORT + 1, 'C': PORT + 2}

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

class Client:
    def __init__(self, host, port, replica_ids=PORTS):
        self.host = host
        self.port = port
        self.username = ''
        self.replica_ids = replica_ids

    def create_account(self, username):
        '''Create new account.'''
        self.username = username
        return self.send_message('0', username)

    def login(self, username):
        '''Log in to existing account.'''
        self.username = username
        self.send_message('1', username)

    def list_all_users(self):
        '''Get a list of all users currently logged in.'''
        return self.send_message('5')

    def send_message(self, opcode, target=None, message=None, doTime=False):
        start = time.time()
        '''Send message to server with opcode, username, message, and target.'''
        with grpc.insecure_channel(str(self.host) + ':' + str(self.port)) as channel:
            stub = messages_pb2_grpc.ServerStub(channel)
            request = messages_pb2.MessageToServer(
                opcode=str(opcode), username=self.username, target=target, message=message
                )
            try:
                response = stub.ReceiveMessageFromClient(request)
            except grpc.RpcError as e: 
                # kTODO: detect if server is down, need to contact new leader
                print("Server is down")
                
                # check if any ports are left
                if self.port == PORT+2:
                    print("all servers have died")
                    log_out = True
                    exit()
                else: 
                    # ask next port if it's the leader 
                    while True:
                        self.port += 1
                        try:
                            response = self.send_message('6')
                        except grpc.RpcError as e:
                            print("Server is down")
        
        data = response.message
        if "SERVER%Kill" in data:
            # Server has sent a signal to kill the client because of an invalid request
            # (i.e. logging into an account which doesnt exist)
            print(data.replace("SERVER%Kill", "").replace("|", ""))
            log_out = True
            exit()
        elif data:
            # print("size of response: ", sys.getsizeof(response))
            print(f"{data}")
        
        end = time.time()
        if doTime:
            print("request + response time: ", end - start)
        return response

    def welcome_menu(self):
        '''Welcome menu for new users.'''
        print(bcolors.OKBLUE + '''
 __     __     ______     __         ______     ______     __    __     ______
/\ \  _ \ \   /\  ___\   /\ \       /\  ___\   /\  __ \   /\ "-./  \   /\  ___\ 
\ \ \/ ".\ \  \ \  __\   \ \ \____  \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  __\ 
 \ \__/".~\_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ 
  \/_/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/

''' + bcolors.ENDC )
        printb('Home Page | Type 0 to create an account or 1 to log in.')

        valid = False
        while valid is False:
            response = input().replace(" ", "")
            if response == '0':
                # create account
                printb('Please enter your username.')
                self.create_account(get_username())
                valid = True

            elif response == '1':
                # log in
                printb('Please enter your username.')
                self.login(get_username())
                valid = True

            else:
                print('Invalid input. Please try again.')

    def query_message(self):
        '''Obtain message details from user and send to server.'''
        printb('Please enter username of recipient.')
        target = get_username()
        printb('Please enter your message.')
        message = get_message()
        self.send_message('2', target, message)

    def logout(self):
        '''Log out of account by closing connection to server.'''
        self.send_message('3')
        exit()


def threaded_receive(client):
    '''Thread function for receiving messages from server via polling.'''
    while True:
        client.send_message('6')
        time.sleep(1)

def Main():
    '''Main messaging loop.'''

    # create new client instance
    client = Client(HOST, PORT)

    # start thread for receiving messages in background
    start_new_thread(threaded_receive, (client,))

    # log in / create account
    client.welcome_menu()

    try:

        while True:
            # sleep for a moment to improve user experience
            time.sleep(0.5)

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
            elif op == "4":
                # delete account
                client.send_message('4')
                client.logout()
            elif op == "5":
                # list all users
                client.list_all_users()
            else:
                printb('Invalid input. Please try again.')
    
    except KeyboardInterrupt as e:
        # Ensure client is properly logged out if user presses Ctrl+C
        client.logout()


if __name__ == '__main__':
    logging.basicConfig()
    Main()
