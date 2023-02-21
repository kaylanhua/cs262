# set up information
project members: kayla huang and tom cobley

## file structure
The relevant file structure for this project looks like the following:

```
design1
├── socket                  # Non gRPC chat server code 
│   ├── server.py          
│   └── client.py        
├── grpc                    # gRPC chat server code 
│   ├── grpc_server.py          
│   ├── grpc_client.py
│   └── messages.proto      # Proto file for auto generation
├── test                    # Test files 
│   ├── benchmarks          # Load and stress tests
│   ├── integration         # End-to-end, integration tests 
│   └── unit                # Unit tests
├── docs                    # Documentation files 
│   ├── engineering.md      # Engineering ledger
│   ├── documentation.md    # Explanations of eng decisions
│   ├── project_specs.md    # Specs for future reference (from Canvas)
│   └── README.md           # instructions for set up
└── environment.yml         # dependencies
```

## Running non-gRPC code
Prerequisites:
- Create conda environment from environment.yml
- Start the conda environment with all packages installed

### One Machine
To run the server, locate to the socket folder and edit the server.py file to have global variable host set to 'localhost' and port set to some N where N > 1024. Then, set the host and port to the same values inside of client.py.

Finally, in one terminal, start the server by running the following command
``` $ python server.py ```

and start the client in another terminal with the command
``` $ python client.py ```

Then, everything is ready to go.

### Across Machines
In server.py, set host to '0.0.0.0' and port to N where N > 1024. Then, run the following command on the computer which the server will be hosted and ran.
``` $ ipconfig getifaddr en0 ```

This will provide the IP address of the computer which the server is being run on. Then, on the client machine, replace the host variable with that IP address (and the port with the same N).

Then, run the files as outlined above. 


## Running gRPC code
To run the gRPC code, navigate to the grpc folder in the repository. Then, inside of that folder, run the command
``` $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto ```

This will generate the _pb2_grpc.py and _pb2.py from the messages.proto file. 

Then, from the grpc_server.py, set the host and port to the same thing as in grpc_client.py (if running on one machine) and run the two files using the instructions above replacing server.py with grpc_server.py and same for the client file. If you are running in two machines, follow the instructions above. 
