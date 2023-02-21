"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import grpc
import messages_pb2
import messages_pb2_grpc
import time 
from _thread import start_new_thread

from clean_client import get_username, get_message

host = 'localhost'  # put in ip address of external server
port = '50051'

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = ''

    def send_message(self, opcode, target=None, message=None):
        with grpc.insecure_channel(host + ':' + port) as channel:
            stub = messages_pb2_grpc.ServerStub(channel)
            request = messages_pb2.MessageToServer(
                opcode=opcode, username=self.username, target=target, message=message
                )
            response = stub.ReceiveMessageFromClient(request)
        if response.message:
            print(response.message)
        return response

    def welcome_menu(self):
        print("------------------")
        print("ⓦ ⓔ ⓛ ⓒ ⓞ ⓜ ⓔ ​​​​​")
        print("------------------")
        print('Home Page | Type 0 to create an account or 1 to log in.')

        valid = False
        while valid is False:
            response = input().replace(" ", "")
            if response == '0' :
                # create account or login (same effect)
                print('Please enter your username.')
                self.username = get_username()
                self.send_message('0')
                valid = True
                
            elif response == '1':
                print('Please enter your username.')
                self.username = get_username()
                self.send_message('1')
                valid = True

            else:
                print('Invalid input. Please try again.')
                
    def query_message(self):
        print('Please enter username of recipient.')
        target = get_username()
        print('Please enter your message.')
        message = get_message()
        self.send_message('2', target, message)
        
    def logout(self):
        exit()


def threaded_receive(client):
    while True:
        client.send_message('6')
        time.sleep(1)

def Main():
    
    client = Client(host, port)
    start_new_thread(threaded_receive, (client,))
    client.welcome_menu()
    
    while True:
        # MENU
        time.sleep(0.5)
        print('Select an option: 2 for send message, 3 for log out, 4 for delete account, 5 for list all users.')
        op = input().replace(" ", "")
        if op == "2":
            client.query_message()    
        elif op == "3":
            # logout
            client.send_message('3')
            client.logout()
        elif op == "4":
            # delete account
            client.send_message('4')
            client.logout()
        elif op == "5":
            # list all users
            client.send_message('5')
        else: 
            print('Invalid input. Please try again.')
        
        


if __name__ == '__main__':
    logging.basicConfig()
    Main()