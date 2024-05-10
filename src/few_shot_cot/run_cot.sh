#!/bin/bash

tasks=("svamp")
models=("meta-llama/Llama-2-7b-chat-hf" "mistralai/Mistral-7B-Instruct-v0.2" "meta-llama/Llama-3-8b-chat-hf") 

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