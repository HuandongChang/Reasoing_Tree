import sys
sys.path.append(".")

from models.TogetherAI_API import call_TogetherAI
from utils.helpers import read_json, load_prompt_template, regex_calibrate, fix_seeds, setup_logging
from utils.helpers import setup_data_loader, answer_cleansing, is_number
from utils.arg_parser import get_parser

import json
from tqdm import tqdm
import re
import os

few_shot_cot = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\nA: Let's think step by step. There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.\n\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\nA: Let's think step by step. There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5.\n\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\nA: Let's think step by step. Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.\n\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\nA: Let's think step by step. Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8.\n\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\nA: Let's think step by step. Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9.\n\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?\nA: Let's think step by step. There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is 29.\n\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\nA: Let's think step by step. Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is 33.\n\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\nA: Let's think step by step. Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is 8.\n\n"

def generate_response(input, model, tokenizer):
    if args.use_together_ai:
        return call_TogetherAI(input, model)
    else:
        return 0

def do_few_shot_cot_generation(args):
    if args.num_consistency > 1:
        assert args.method == 'few_shot_cot', 'only few_shot_cot supports self_consistency'

    dataloader = setup_data_loader(args)

    if args.use_together_ai:
        tokenizer, model = None, args.model_ckpt
    else:
        pass
        

    total = 0
    correct_list = []      

    jsonl_model_response = []
    jsonl_correct = []  
    gt_lst = []
    pred_lst = []
    id = []
    questions=[]

    for i, data in tqdm(enumerate(dataloader), total=min(args.num_examples,len(dataloader))):
        if i>=args.num_examples:
            break

        if args.verbose:
            print(' ')
            print("{}st data".format(i+1))
                
        # Prepare question template ...
        question, y = data
        x = "Q: " + question[0] + "\n" + "A:"
        y = y[0].strip()
        
        if args.method == "zero_shot":
            x = x + " " + 'The answer (arabic numerals) is'
        elif args.method == "zero_shot_cot":
            x = x + " " + "Let's think step by step."
        elif args.method == "few_shot_cot":
            x = few_shot_cot + x
        else:
            raise ValueError("method is not properly defined ...")
        
        # Answer prediction by generating text ...


        z = []
        for _ in range(args.num_consistency):
            z.append(generate_response(x, model, tokenizer))
        

        # Answer extraction for zero-shot-cot ...
        if args.method == "zero_shot_cot":
            z2 = x + z[0] + " " + '\nTherefore, the answer (arabic numerals) is'
            pred = generate_response(z2, model, tokenizer)
            if args.verbose:
                print(z2 + pred)
        else:
            pred = z if args.num_consistency > 1 else z[0]
            if args.verbose and args.num_consistency == 1:
                print(x + pred)
        # breakpoint()

        # Clensing of predicted answer ...n
        if args.num_consistency == 1:
            pred, model_response = answer_cleansing(args, pred)
        else: 
            preds, model_response = {}, None
            for p in pred:
                p_after, model_response = answer_cleansing(args, p)
                preds[p_after] = preds.get(p_after, 0) + 1
            sorted_items = sorted(preds.items(), key=lambda item: item[1], reverse=True)
            pred = sorted_items[0][0]
    
        jsonl_model_response.append(model_response)

        # Choose the most frequent answer from the list ...
        if args.verbose:
            print("pred : {}".format(pred))
            print("GT : " + y)
            print(' ')

        pred = pred.replace(',','').replace('\n', '')
        gt = y.replace(',','').replace('\n', '')
        gt_lst.append(gt)
        pred_lst.append(pred)
        id.append(i+1)
        questions.append(question[0])
        
        # Checking answer ...
        if is_number(pred):
            correct = int(float(pred) == float(gt))
        else:
            correct = 0
        correct_list.append(correct)
        jsonl_correct.append(correct)
        total += 1 

        if (args.limit_dataset_size != 0) and ((i+1) >= args.limit_dataset_size):
            break
    
    # Calculate accuracy ...
    accuracy = (sum(correct_list) * 1.0 / total) * 100
    print("accuracy : {} %".format(accuracy))

    # Record result
    try:
        # Record result
        model = args.model_ckpt.split("/")[-1]
        file_name = f"out/{args.dataset_name}_{args.method}_{model}.json"
        combined_list = [{"id":i, "question":q, "groud_truth_answer":gt,'model_response': response,'model_answer': p, 'correct': c} 
                         for i, q, gt, response, p, c in zip(id, questions, gt_lst, jsonl_model_response, pred_lst, jsonl_correct)]

        # Check if the 'out' directory exists and create it if it doesn't
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the results to the file
        with open(file_name, 'w') as file:
            json.dump(combined_list, file)
    except:
        model = args.model_ckpt.split("/")[-1]
        file_name = f"out/{args.dataset_name}_{args.method}_{model}.json"
        combined_list = [{'answer': a, 'correct': c} for a, c in zip(jsonl_model_response, jsonl_correct)]
        with open(file_name, 'w') as file:
            json.dump(combined_list, file)

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    fix_seeds(args.seed)
    do_few_shot_cot_generation(args)
