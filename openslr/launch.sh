#!/usr/bin/env bash

#source ./venv/bin/activate
source $HOME/python2env/bin/activate

export PYTHONUNBUFFERED=1
export DATA_PATH="/home/ishtar/data/goodailab/OpenSlr"
export AWS_ACCESS_KEY_ID="AKIAIKJF7CPTFBH4ZT5A"
export AWS_SECRET_ACCESS_KEY="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"
export WORKER_HOSTS="127.0.0.1:3002,127.0.0.1:3003"
export PS_HOSTS="127.0.0.1:3001"
export CLUSTER='{"ps": ["127.0.0.1:3001"], "worker": ["127.0.0.1:3002", "127.0.0.1:3003"], "master": ["127.0.0.1:3002"]}'

COMMAND="main.py"
NOHUP_OUT="./output"

TF_CONFIG_MASTER='{"environment": "cloud", "cluster": '$CLUSTER', "task": {"type": "master", "index": 0}}'
CUDA_VISIBLE_DEVICES=0 TF_CONFIG=$TF_CONFIG_MASTER python $COMMAND >> "$NOHUP_OUT-master" 2>&1 &
PID_MASTER=$!

TF_CONFIG_WORKER_1='{"environment": "cloud", "cluster": '$CLUSTER', "task": {"type": "worker", "index": 1}}'
CUDA_VISIBLE_DEVICES=1 TF_CONFIG=$TF_CONFIG_WORKER_1 python $COMMAND >> "$NOHUP_OUT-worker1" 2>&1 &
PID_WORKER=$!

TF_CONFIG_PS_0='{"environment": "cloud", "cluster": '$CLUSTER', "task": {"type": "ps", "index": 0}}'
CUDA_VISIBLE_DEVICES= TF_CONFIG=$TF_CONFIG_PS_0 python $COMMAND >> "$NOHUP_OUT-ps1" 2>&1 &
PID_PS=$!

echo "wait for $PID_MASTER, kill $PID_WORKER, $PID_PS"
wait $PID_MASTER
kill $PID_WORKER
kill $PID_PS
