from argparse import ArgumentParser
from pathlib import Path


def get_parser():
    parser = ArgumentParser()
    
    parser.add_argument("--seed", default=1)
    parser.add_argument("--verbose", action='store_true', default=False)
    parser.add_argument("--use_together_ai", action='store_true')
    parser.add_argument("--use_hf_api", action='store_true')
    parser.add_argument("--use_vllm_api", action='store_true')
    parser.add_argument("--model_parallel", action='store_true')
    parser.add_argument("--log_header", default="default")
    
    #! LLM settings
    parser.add_argument('--max_tokens', type=int,
                        default=256, help='max_tokens')
    parser.add_argument('--temperature', type=float,
                        default=0.8, help='temperature')
    parser.add_argument('--top_k', type=int, default=40, help='top_k')
    parser.add_argument('--top_p', type=float, default=0.95, help='top_p')
    parser.add_argument('--num_beams', type=int, default=1, help='num_beams')
    # parser.add_argument('--repetition_penalty', type=float, default=1.1, help='repetition_penalty')
    parser.add_argument('--num_consistency', type=int,
                        default=1, help='self_consistency')
    
    #! path and names
    parser.add_argument("--data_root", default=Path("./data"))
    parser.add_argument("--log_root", default=Path("./out"))
    parser.add_argument("--prompts_root", default=Path("./prompts"))
    
    parser.add_argument("--model_ckpt", required=True)
    parser.add_argument("--dataset_name", required=True)
    parser.add_argument("--limit_dataset_size", type=int, default=0, help="whether to limit test dataset size. if 0, the dataset size is unlimited and we use all the samples in the dataset for testing.")
    
    parser.add_argument("--note", default="")
    parser.add_argument("--method", type=str, default="zero_shot_cot", choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot"], help="method")
    parser.add_argument("--max_num_worker", type=int, default=3, help="maximum number of workers for dataloader")
    
    parser.add_argument("--num_examples", type=int, default=10000)
    return parser