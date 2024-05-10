import re
import os
import sympy
import pandas as pd
from pathlib import Path
from utils.helpers import read_json
from prompts.gsm8k_rt import *


def get_current_numbers(y: str) -> str:
    last_line = y.strip().split('\n')[-1]
    return last_line.split('left: ')[-1].split(')')[0]


class SVMPTask():

    def __init__(self):
        data_root = Path("./data")
        self.data = read_json(os.path.join(data_root, 'SVAMP', 'test_with_ids.json'))
        self.value_cache = {}
        self.steps = 6
        self.stops = ["\n", "\n\n"]

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]['question']
    
    def extract_answer(self, preds: str):
        preds = preds.split('The answer is')
        answer_flag = True if len(preds) > 1 else False 
        if answer_flag:
            pred = preds[1]
        else:
            pred = preds[-1]

        pred = pred.replace(",", "")
        pred = [s for s in re.findall(r'-?\d+\.?\d*', pred)]

        if len(pred) == 0:
            pred = ""
        else:
            if answer_flag:
                pred = pred[0]
            else:
                pred = pred[-1]
        if pred != "" and pred[-1] == ".":
                pred = pred[:-1]
        pred = pred.replace(',','').replace('\n', '')
        if self.is_number(pred):
            return float(pred)
        else:
            print(pred)
            return 0
    
    def is_number(self, s):    
        try:      
            float(s)        
            return True    
        except ValueError:  
            pass  
        try:        
            import unicodedata  
            unicodedata.numeric(s) 
            return True    
        except (TypeError, ValueError):        
            pass    
        return False
    
    def get_gt(self, question_asnwer):
        return str(question_asnwer)

    def test_output(self, idx: int, output: str):
        model_answer = self.extract_answer(output)
        gt = self.get_gt(self.data[idx]["answer"])

        if self.is_number(model_answer):
            correct = int(float(model_answer) == float(gt))
        else:
            correct = 0

        return {'r': correct}
        
    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x).strip() + y
    
    @staticmethod
    def vote_prompt_wrap(x: str, ys: list) -> str:

        def remove_step_notations(text):
            pattern = r"Step [1-9]:\s*"
            cleaned_text = re.sub(pattern, "", text)
            return cleaned_text
        
        prompt = vote_prompt
        prompt = prompt.format(instruction=x).strip()
        for i, y in enumerate(ys, 1):
            y = remove_step_notations(y)
            y = y.replace('\n', ' ')
            y = y.replace('  ', '')
            prompt += f'\nChoice {i}:{y}'
        prompt += "\n" + "Response:"
        return prompt
    
    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        vote_results = [0] * n_candidates
        for vote_output in vote_outputs:
            numbers = re.findall(r"best choice is (\d+)", vote_output)
            if numbers:
                vote = int(numbers[-1]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
            # else:
            #     print(f'vote no match: {[vote_output]}')
        return vote_results