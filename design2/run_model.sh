#!/bin/bash

# Kill previous run 
pkill -f main.py

python main.py --id=A --ticks_ps=2 &
python main.py --id=B --ticks_ps=5 &
python main.py --id=C --ticks_ps=1 &

wait