#!/bin/bash

# Kill previous run
pkill -f main.py

# Run servers
# ttab -w 'conda activate 262 ; python main.py --id=A' &
# ttab -w 'conda activate 262 ; python main.py --id=B' &
# ttab -w 'conda activate 262 ; python main.py --id=C' &
ttab -w 'conda activate 262 ; python main.py --id=D' &
ttab -w 'conda activate 262 ; python main.py --id=E' &

sleep 5

# Run clients
# ttab -w 'conda activate 262 ; python grpc_client.py' &
ttab -w 'conda activate 262 ; python grpc_client.py' &
