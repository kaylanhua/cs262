#!/bin/bash

# Kill previous run 
pkill -f main.py

TICKS_PS_A=1
TICKS_PS_B=1
TICKS_PS_C=1

P_INTERNAL=0.3

OUT_DIR="run-ticks-$TICKS_PS_A-$TICKS_PS_B-$TICKS_PS_C--p-$P_INTERNAL"

mkdir -p $OUT_DIR

python main.py --id=A --ticks_ps=$TICKS_PS_A --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &
python main.py --id=B --ticks_ps=$TICKS_PS_B --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &
python main.py --id=C --ticks_ps=$TICKS_PS_C --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &

wait