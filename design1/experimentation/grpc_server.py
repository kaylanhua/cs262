# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import messages_pb2
import messages_pb2_grpc

# from clean_server import create_account, login, send_pending

sessions = dict()
messages = dict()

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


class Server(messages_pb2_grpc.ServerServicer):
    
    def send_pending(self, messages, username):
        toClient = ''
        if username in messages:
            info_msg = f"You have {len(messages[username])} new messages since you last logged in:\n"
            toClient += info_msg

            # TODO: reads may happen together

            for sender, message in messages[username]:
                toClient += f"[{sender}] {message}\n"
            messages.pop(username)
        return toClient
    
    def ReceiveMessageFromClient(self, request, context):
        print(str(request))
        opcode = request.opcode
        username = request.username
        target = request.target
        message = request.message
        toClient = ''
        # CREATE ACCOUNT
        if opcode == '0':
            if username in sessions:
                # user alr exists, log in
                login(username, True)
                # TODO: raise exception, user already exists
            else:
                # user does not exist yet, create new user and log in
                create_account(username, True)
                toClient = f"Welcome to your new account, {username}"
        
        # LOG IN
        elif opcode == '1': # log in
            login(username, True)
            toClient = f"Welcome back, {username}\n"
            # Send undelivered messages, if any
            toClient += self.send_pending(messages, username)
        
        # SEND MESSAGE    
        elif opcode == '2':
            if target not in sessions.keys():
                # TODO: raise exception instead?
                toClient = f"Error: User {target} does not exist. Message could not be sent"
            else: 
                if sessions[target] == None: 
                    # target is not logged in, queue message
                    queue_message(username, target, message)
                else:
                    # send message to target
                    print(f"someone is trying to send a message to {target}")
                    # TODO to_client(target, message, username)
        
        # LOG OUT            
        elif opcode == '3': 
            toClient = "You have logged out. Goodbye!"
            logout(username)

        # DELETE ACCOUNT    
        elif opcode == '4':
            toClient = "Your account has been deleted. Goodbye!"
            sessions.pop(username)
            if username in messages:
                messages.pop(username)
        
        # LIST ALL USERS    
        elif opcode == '5':
            toClient = "[ALL ACCOUNTS]" + str(list(sessions.keys()))

        return messages_pb2.ServerLog(message=toClient)
    
    # def SendMessageToClient(self, request, context):
    #     return messages_pb2.MessageToClient(usernameOrStatus="0", message="hi")
    
    # def QueueMessage(self, request, context):
    #     return messages_pb2.ServerLog(message="hello %s, you have queued a message" % request.username)
    
    # def SeeAllAccounts(self, request, context):
    #     return messages_pb2.MessageToClient(usernameOrStatus="0", message="all accounts")
    

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messages_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()