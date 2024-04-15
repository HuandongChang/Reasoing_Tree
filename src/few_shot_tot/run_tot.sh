#!/bin/bash

models=("/home/ms/mingyuan/model_hf/Llama-2-7b-hf" "/home/ms/mingyuan/model_hf/Llama-2-13b-chat-hf")

for model in "${models[@]}"; do
    echo CUDA_VISIBLE_DEVICES=0 python src/few_shot_tot/run_tot.py \
        --model "$model" 

    CUDA_VISIBLE_DEVICES=0 python src/few_shot_tot/run_tot.py \
        --model "$model" 
done



python3 src/few_shot_tot/run_tot.py \
        --model "togethercomputer/llama-2-7b" \
        --use_together_ai
