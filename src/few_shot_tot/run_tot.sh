#!/bin/bash

tasks=("gsm8k" "multiarith" "SVAMP")
models=("meta-llama/Llama-3-70b-chat-hf" "mistralai/Mixtral-8x7B-Instruct-v0.1" "meta-llama/Llama-3-8b-chat-hf")

for task in "${tasks[@]}"; do
    for model in "${models[@]}"; do
        echo "Running task: $task with model: $model"
        echo python3 src/few_shot_tot/run_tot.py \
                --model "$model" \
                --use_together_ai \
                --task "$task"

        python3 src/few_shot_tot/run_tot.py \
                --model "$model" \
                --use_together_ai \
                --task "$task"
    done
done