#!/bin/bash

tasks=("SVAMP")
models=("meta-llama/Llama-2-7b-chat-hf" "mistralai/Mistral-7B-Instruct-v0.2" "meta-llama/Llama-3-8b-chat-hf") 

for task in "${tasks[@]}"; do
    for model in "${models[@]}"; do
        echo "Running task: $task with model: $model"
        echo python3 src/reasoning_tree/run_rt.py \
                --model "$model" \
                --use_together_ai \
                --task "$task"

        python3 src/reasoning_tree/run_rt.py \
                --model "$model" \
                --use_together_ai \
                --task "$task"
    done
done
