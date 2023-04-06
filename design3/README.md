# design exercise three
fault tolerant chat server
students: kayla huang and tom cobley



## Running gRPC code
To run the gRPC code, navigate to the grpc folder in the repository. Then, inside of that folder, run the command
``` $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto ```

This will generate the _pb2_grpc.py and _pb2.py from the messages.proto file. 

Then, from the grpc_server.py, set the host and port to the same thing as in grpc_client.py (if running on one machine) and run the two files using the instructions above replacing socket_server.py with grpc_server.py and same for the client file. If you are running in two machines, follow the instructions above. 
