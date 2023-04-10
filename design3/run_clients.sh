#!/bin/bash

# Kill previous run
pkill -f grpc_client.py

ttab -w python grpc_client.py &
ttab -w python grpc_client.py &
ttab -w python grpc_client.py &

wait
