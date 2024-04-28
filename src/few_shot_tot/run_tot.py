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
    samples = generate(args, model, tokenizer, prompt, n_sample=n_generate_sample, stop=stop, max_tokens=32, temperature=0.8)
    out = []
    for sample in samples:
        cur_branch = y + sample + '\n'
        out.append(cur_branch)
    return out

def solve(args, task, idx, model, tokenizer):
    fix_seeds(1)
    x = task.get_input(idx)  
    ys = ['\n']  
    final_ys = []
    paths = []
    for _ in range(task.steps):
        if not ys:
            break
        # generate
        new_ys = [get_samples(args, model, tokenizer, task, x, y, args.n_generate_sample, stop=task.stops) for y in ys]
        new_ys = list(itertools.chain(*new_ys))
        ids = list(range(len(new_ys)))

        # # evaluation
        # values = get_votes(args, model, tokenizer, task, x, new_ys, args.n_evaluate_sample)

        # # selection
        # ps = np.array(values) / sum(values)
        # try:
        #     select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        # except:
        #     select_ids = np.random.choice(ids, size=args.n_select_sample).tolist()

        select_ids = np.random.choice(ids, size=args.n_select_sample).tolist()

        if args.verbose:
            print(new_ys[:])
            print("")
            print(select_ids)

        select_new_ys = [new_ys[select_id] for select_id in select_ids]
        paths.append(select_new_ys[:])
        if args.verbose:
            print("")
            print(select_new_ys[:])
            print("")

        pruned_branch_ids = []
        for i in range(len(select_new_ys)):
            if "The answer is" in select_new_ys[i]:
                final_ys.append(task.extract_answer(select_new_ys[i]))
                pruned_branch_ids.append(i)

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
        # solve
        model_answer, paths = solve(args, task, i, model, tokenizer)
        if args.verbose:
            print("model_asnwer: ", model_answer)
        # gt
        if args.task == "gsm8k":
            gt = task.get_gt(task.data[i]["answer"])
        elif args.task == "multiarith":
            gt = task.get_gt(task.data[i]["final_ans"])
        elif args.task == "SVAMP":
            gt = task.get_gt(task.data[i]["Answer"])
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
    file_name = f"out/{args.task}_tot_{model}.json"
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
    args.add_argument('--n_evaluate_sample', type=int, default=3)
    args.add_argument('--n_select_sample', type=int, default=3)
    args.add_argument("--use_together_ai", action='store_true')
    args.add_argument("--verbose", action='store_true')
    args.add_argument("--model", required=True)
    args = args.parse_args()
    a = "Given a question, your task is to decompose it into manageable sub-questions. For each sub-question, summarize existing information, determine the new information required, and then articulate a logical and useful sub-question that brings you closer to the final answer. Conclude each answer with \"The answer is\". When ready to address the original question, your final sub-question should contain \"Now we can answer the question: \", leading to a detailed answer that encapsulates all the insights gained, always ending with \"The answer is\".\n\nQuestion 1: Four years ago, Kody was only half as old as Mohamed. If Mohamed is currently twice as 30 years old, how old is Kody?\nQuestion 1.1: We start by understanding that four years ago, Kody's age was half that of Mohamed's, and currently, Mohamed is twice 30 years old. To proceed, we need Mohamed's current age. Therefore, the next useful subquestion we need to solve is: What is Mohamed's current age?\nAnswer 1.1: Since Mohamed is currently twice 30, we calculate 2 * 30 = 60. Thus, Mohamed is 60 years old now. The answer is 60.\nQuestion 1.2: With the information that Mohamed is 60 years old, we next need to find out his age four years ago to better understand the age difference between him and Kody at that time. Therefore, the next useful subquestion we need to solve is: What was Mohamed's age four years ago?\nAnswer 1.2: Mohamed's age four years ago is found by performing the calculation 60 - 4 = 56. Mohamed was 56 years old four years ago. The answer is 56.\nQuestion 1.3: Knowing that Mohamed was 56 years old four years ago enables us to figure out Kody's age at that time, given that Kody was half as old as Mohamed. Therefore, the next useful subquestion we need to solve is: How old was Kody four years ago?\nAnswer 1.3: If Kody was half as old as Mohamed four years ago, then 56 / 2 = 28. Kody was 28 years old four years ago. The answer is 28.\nQuestion 1.4: With the information that Kody was 28 years old four years ago, the final piece of information we need is his current age. Now we can answer the question: How old is Kody now?\nAnswer 1.4: Kody was 28 years old four years ago. Adding those four years to his age, we calculate 28 + 4 = 32. Kody is now 32 years old. The answer is 32.\n\nQuestion 2: On a moonless night, three fireflies danced in the evening breeze. They were joined by four less than a dozen more fireflies before two of the fireflies flew away. How many fireflies remained?\nQuestion 2.1: We start with the initial information that three fireflies were present, and then they were joined by four less than a dozen more fireflies. To proceed, we need to calculate the total number of fireflies that joined. Therefore, the next useful subquestion we need to solve is: How many fireflies joined the initial three?\nAnswer 2.1: A dozen fireflies minus four gives us 12 - 4 = 8 fireflies that joined the initial three. The answer is 8.\nQuestion 2.2: With the knowledge that 8 fireflies joined the initial 3, we next need to find out the total number of fireflies before any of them flew away. Therefore, the next useful subquestion we need to solve is: What was the total number of fireflies before two flew away?\nAnswer 2.2: The total number of fireflies before any flew away can be found by adding the initial three to the eight that joined, which gives us 3 + 8 = 11 fireflies. The answer is 11.\nQuestion 2.3: Knowing that there were 11 fireflies before two flew away gives us the information needed to determine how many remained. Now we can answer the question: How many fireflies remained after two flew away?\nAnswer 2.3: From the 11 fireflies, if two flew away, we subtract two from the total, which gives us 11 - 2 = 9 fireflies remaining. The answer is 9.\n\nQuestion 3: Ali has four 10 dollar bills and six 20 dollar bills that he saved after working for Mr. James on his farm. Ali gives his sister half of the total money he has and uses 3/5 of the remaining amount of money to buy dinner. Calculate the amount of money he has after buying the dinner.\nQuestion 3.1: We start with Ali having four 10 dollar bills and six 20 dollar bills. To proceed, we first need to calculate the total amount of money Ali has from these bills. Therefore, the next useful subquestion we need to solve is: What is the total amount of money Ali has from the 10 and 20 dollar bills?\nAnswer 3.1: The total amount from the ten dollar bills is 4 * 10 dollars = 40 dollars, and from the twenty dollar bills is 6 * 20 dollars = 120 dollars. Adding these amounts gives us 40 dollars + 120 dollars = 160 dollars. The answer is 160.\nQuestion 3.2: With the total of 160 dollars, we next need to find out how much money Ali gives to his sister, which is half of his total money. Therefore, the next useful subquestion we need to solve is: How much money does Ali give to his sister?\nAnswer 3.2: Ali gives half of his total money to his sister, which calculates to 160 / 2 = 80 dollars. The answer is 80.\nQuestion 3.3: Knowing that Ali has given 80 dollars to his sister, leaving him with 80 dollars, we now aim to determine how much money he uses to buy dinner, which is 3/5 of the remaining amount. Therefore, the next useful subquestion we need to solve is: How much money does Ali use to buy dinner?\nAnswer 3.3: Ali uses 3/5 of the remaining 80 dollars to buy dinner, which calculates to (3/5) * 80 = 48 dollars. The answer is 48.\nQuestion 3.4: With the information that Ali used 48 dollars to buy dinner from the remaining 80 dollars, the final piece of information we need is how much money he has left after this purchase. Now we can answer the question: How much money does Ali have after buying the dinner?\nAnswer 3.4: After buying dinner for 48 dollars out of the remaining 80 dollars, Ali has 80 - 48 = 32 dollars left. The answer is 32.\n\nQuestion 4: Linda makes and sells necklaces at craft fairs. At her most recent fair she sold 4 necklaces and 8 rings for a total of 80 dollars. If each necklace costs 12 dollars, how much does each ring cost?\nQuestion 4.1: We start with Linda selling 4 necklaces at 12 dollars each and 8 rings for a total of 80 dollars. The first step is to calculate the total sales from the necklaces. Therefore, the next useful subquestion we need to solve is: What is the total sales amount from the necklaces?\nAnswer 4.1: The total sales from the necklaces can be calculated by 4 * 12 = 48 dollars. Linda made 48 dollars from selling the necklaces. The answer is 48.\nQuestion 4.2: Knowing that Linda made 48 dollars from the necklaces and the total sales were 80 dollars, we need to find out the total sales from the rings. Therefore, the next useful subquestion we need to solve is: What is the total sales amount from the rings?\nAnswer 4.2: The total sales from the rings can be calculated by subtracting the necklace sales from the total sales, which gives us 80 - 48 = 32 dollars. Linda made 32 dollars from selling the rings. The answer is 32.\nQuestion 4.3: With the information that the total sales from the rings were 32 dollars and there were 8 rings sold, we need to calculate the cost of each ring. Now we can answer the question: How much does each ring cost?\nAnswer 4.3: The cost of each ring can be calculated by dividing the total ring sales by the number of rings sold, which gives us 32 / 8 = 4 dollars per ring. The answer is 4.\n\n Question: {input}"
    fix_seeds(1)
    run(args)
