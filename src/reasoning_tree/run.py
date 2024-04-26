import os
import json
import argparse

import sys
sys.path.append(".")

from tasks import get_task
# from methods import solve
from tqdm import tqdm
import torch
import random
# from utils.helpers import fix_seeds
import itertools
import numpy as np
from functools import partial
from models.TogetherAI_API import call_TogetherAI
from collections import Counter

def fix_seeds(seed):
    # random
    random.seed(seed)
    # Numpy
    np.random.seed(seed)
    # Pytorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def generate(args, model, tokenizer, prompt, n_sample, stop, max_tokens=512, temperature=0.8):
    out = []
    for _ in range(n_sample):
        cur_out = call_TogetherAI(prompt, model, stop=stop, max_tokens=max_tokens, temperature=temperature)
        out.append(cur_out)
    return out

def get_votes(args, model, tokenizer, task, x, ys, n_evaluate_sample):
    vote_prompt = task.vote_prompt_wrap(x, ys)
    vote_outputs = generate(args, model, tokenizer, vote_prompt, n_sample=n_evaluate_sample, stop=[], max_tokens=128, temperature=0.8)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values

def get_samples(args, model, tokenizer, task, x, y, n_generate_sample, stop):
    prompt = task.cot_prompt_wrap(x, y)
    samples = generate(args, model, tokenizer, prompt, n_sample=n_generate_sample, stop=stop, max_tokens=128, temperature=0.8)
    out = []
    for sample in samples:
        cur_branch = y + sample + '\n'
        out.append(cur_branch)
    return out

def select_optimal_sample(samples, answers):
    answer_counts = Counter(answers)
    most_frequent_answer = max(answer_counts, key=answer_counts.get)
    for sample, answer in zip(samples, answers):
        if answer == most_frequent_answer:
            return sample
    print("select_optimal_sample: No Answer There")
    return samples[0]
        
def get_subquestion_answer(args, model, tokenizer, task, x, y, n_generate_sample, stop):
    prompt = task.cot_prompt_wrap(x, y)
    samples = generate(args, model, tokenizer, prompt, n_sample=args.n_evaluate_sample, stop=stop, max_tokens=128, temperature=0.8)  
    answers = [task.extract_answer(sample) for sample in samples]
    best_sample = select_optimal_sample(samples, answers)
    return best_sample

def solve(args, task, idx, model, tokenizer):
    fix_seeds(1)
    x = task.get_input(idx)  
    ys = ['\n']  
    final_ys = []
    paths = []
    for _ in range(task.steps):
        if not ys:
            break
        # generate subquestion
        new_ys = [get_samples(args, model, tokenizer, task, x, y, args.n_generate_sample, stop=task.stops) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        if args.verbose:
            print("new_ys: ", new_ys[:])
            print(len(new_ys))
            print("")
        
        # generate answer for those subquestions
        new_as = [get_subquestion_answer(args, model, tokenizer, task, x, y, args.n_generate_sample, stop=task.stops) for y in new_ys]
        if args.verbose:
            print("new_as: ", new_as[:])
            print(new_as)
            print("")

        # update ys
        new_ys = [y + a + "\n" for y, a in zip(new_ys, new_as)]
        ids = list(range(len(new_ys)))

        if args.enable_votes:
            # evaluation
            values = get_votes(args, model, tokenizer, task, x, new_ys, args.n_evaluate_sample)
            # selection
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        else:
            select_ids = np.random.choice(ids, size=args.n_select_sample).tolist()
        select_new_ys = [new_ys[select_id] for select_id in select_ids]
        paths.append(select_new_ys[:])
        if args.verbose:
            print("select_new_ys: ", select_new_ys[:])
            print(len(select_new_ys))
            print("")
        
        pruned_branch_ids = []
        for i in range(len(select_new_ys)):
            if "Now we can answer the question" in select_new_ys[i]:
                response = select_new_ys[i].split("Now we can answer the question")[-1]
                final_ys.append(task.extract_answer(response))
                pruned_branch_ids.append(i)

        if len(final_ys) > args.n_evaluate_sample:
            break

        pruned_branch_ids.sort(reverse=True)
        for index in pruned_branch_ids:
            select_new_ys.pop(index)
        
        ys = select_new_ys

    if not final_ys:
        for y in ys:
            prompt = task.cot_prompt_wrap(x, y)
            prompt += '''
            Now answer the question directly in one single step. Please start your answer with \"The answer is\"
            '''
            prediction = generate(args, model, tokenizer, prompt, n_sample=1, stop=task.stops)[0]
            prediction = task.extract_answer("The answer is " + prediction)
            final_ys.append(prediction)

    preds = {}
    for final_y in final_ys:
        preds[final_y] = preds.get(final_y, 0) + 1
    sorted_items = sorted(preds.items(), key=lambda item: item[1], reverse=True)
    final_answer = sorted_items[0][0]

    return float(final_answer), paths

def run(args):

    tokenizer, model = None, args.model

    task = get_task(args.task)
    corrects = 0
    total = 0
    all_question_paths = []
    all_question_corrects = []
    pbar = tqdm(range(max(args.task_start_index, 0), min(len(task), args.task_end_index)), desc="Acc: 0.00%")
    for i in pbar:
        if i >= 2:
            break
        # solve
        model_answer, paths = solve(args, task, i, model, tokenizer)
        if args.verbose:
            print("model_asnwer: ", model_answer)
        # gt
        if args.task in ("multiarith"):
            gt = task.get_gt(task.data[i]["final_ans"])
        else:
            gt = task.get_gt(task.data[i]["answer"])
        gt = gt.replace(',','').replace('\n', '')
        gt = float(gt)
        
        if args.verbose:
            print("gt: ", gt)
        # correct
        correct = int(float(model_answer) == float(gt))
        corrects += correct
        all_question_corrects.append(correct)
        all_question_paths.append(paths)
        total += 1
        acc = corrects / total
        pbar.set_description(f"Acc: {acc:.5f}")

    model = args.model.split("/")[-1]
    file_name = f"out/{args.task}_rt_{model}.json"
    combined_list = [{'answer': a, 'correct': c} for a, c in zip(all_question_paths, all_question_corrects)]

    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, 'w') as file:
        json.dump(combined_list, file)

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--temperature', type=float, default=0.8)
    args.add_argument('--task', type=str, default='gsm8k')
    args.add_argument('--task_start_index', type=int, default=0)
    args.add_argument('--task_end_index', type=int, default=float('inf'))
    args.add_argument('--n_generate_sample', type=int, default=3)  
    args.add_argument('--n_evaluate_sample', type=int, default=8)
    args.add_argument('--n_select_sample', type=int, default=2)
    args.add_argument("--use_together_ai", action='store_true')
    args.add_argument("--verbose", action='store_true')
    args.add_argument("--enable_votes", action='store_true')
    args.add_argument("--model", required=True)
    args = args.parse_args()
    fix_seeds(1)
    run(args)

