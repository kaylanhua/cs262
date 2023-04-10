#!/bin/bash

# Kill previous run
pkill -f main.py

# Run servers
ttab -w python main.py --id=A &
ttab -w python main.py --id=B &
ttab -w python main.py --id=C &
# ttab -w python main.py --id=D &
# ttab -w python main.py --id=E &

sleep 1

# Run clients
ttab -w python grpc_client.py &
ttab -w python grpc_client.py &
