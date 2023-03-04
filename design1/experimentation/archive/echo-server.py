import socket
import grpc
import helloworld_pb2

HOST = '127.0.0.1'
PORT = 6000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            
            
            
# def GetFeature(self, request, context):
#   feature = get_feature(self.db, request)
#   if feature is None:
#     return route_guide_pb2.Feature(name="", location=request)
#   else:
#     return feature