#!/bin/bash

# Kill previous run
pkill -f main.py

TICKS_PS_A=6
TICKS_PS_B=6
TICKS_PS_C=6

P_INTERNAL=0.1

OUT_DIR="run-ticks-$TICKS_PS_A-$TICKS_PS_B-$TICKS_PS_C--p-$P_INTERNAL"

mkdir -p $OUT_DIR

python main.py --id=A --ticks_ps=$TICKS_PS_A --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &
python main.py --id=B --ticks_ps=$TICKS_PS_B --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &
python main.py --id=C --ticks_ps=$TICKS_PS_C --out_dir=$OUT_DIR --p_internal=$P_INTERNAL &

wait
