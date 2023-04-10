#!/bin/bash

# Kill previous run
pkill -f main.py

python main.py --id=A &
python main.py --id=B &
python main.py --id=C &

wait
