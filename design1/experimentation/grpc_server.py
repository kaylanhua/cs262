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


class Server(messages_pb2_grpc.ServerServicer):

    # def SayHello(self, request, context):
    #     return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
    
    def CreateAccount(self, request, context):
        return messages_pb2.CreateAccount(request, context)
    
    def LogIn(self, request, context):
        return messages_pb2.LogIn(request, context)


def serve():
    # port = '50051'
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # server.add_insecure_port('[::]:' + port)
    # server.start()
    # print("Server started, listening on " + port)
    # server.wait_for_termination()
    
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