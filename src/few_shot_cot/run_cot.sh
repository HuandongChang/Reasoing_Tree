#!/bin/bash

tasks=("gsm8k" "multiarith" "SVAMP")
models=("meta-llama/Llama-3-70b-chat-hf" "mistralai/Mixtral-8x7B-Instruct-v0.1" "meta-llama/Llama-3-8b-chat-hf")

for task in "${tasks[@]}"; do
    for model in "${models[@]}"; do
        echo "Running task: $task with model: $model"
        echo python3 src/few_shot_cot/run_few_shot.py \
            --model_ckpt "$model"\
            --dataset_name "$task" \
            --method "few_shot_cot" \
            --use_together_ai
        
        python3 src/few_shot_cot/run_few_shot.py \
            --model_ckpt "$model"\
            --dataset_name "$task" \
            --method "few_shot_cot" \
            --use_together_ai
    done
done