import together
from typing import List, Dict
import time

# '1d328918b6c9af31dfafc1c6751890e52481c75866448c9db364a7e58c666814',
# '7b1925f49e33f63f6d64c26a6bbf78ec4373e8d5df205ac785573311a4acd491',
# '3668e80e292c32d8a23ed01bddc8d4efabc786ede0ea7d40d2de3c8ca49d6015',
# 'd16049df3f5732d9bf180f9b0d79947d6c20471bc9d9277166c5b6e180cef5cf',
# "fb9262df6fe23a25f35355b42cc4d3182754fd9d186309aad0cd4f52fe9c8306",
# '31a5be9a66b0bf3e10d877640b7ae5f73464949c157d7d01cdb6de1f16f53fbb',
# 'df2fbd8b27413e6a3b5d87a8df44c0ccfc7a175d19445a5f92a9a29450c1ec53',
# 'd202990ef50e94b0df994bc9d35f75cfe90f91f4aa126b08e33dd391d3e4a4e6',
# "c9ea3ceced7d13f297a2388e48565ade965e451df25910e31e8a32919603ae92",
# "045d2cf90a4ebca1997ee66acd5ea0d0fc83c99b281429ca21af42e486fe4be0",
# "d3a3fd41900ad88e52855d0100e128a089eec5fa4e65818453ec9a41077fcf01",
# "380775a5d7ac61cce84c5aefad7f0b28ec83bebb94632ad01e227ec1f0a3c34e",
# "1ef5fdc7f7e072f3280886dcb9b7883187cee93a87dd40a37cf6602ee39850d4",
# "acc82a8f44d765ce1462a2e047e5e6d1c434a4f5974d12e1aa526320cf552969",

keys = [
    "6e3ac9ec855ba22ae3e37b7fbd105d6766ca9c14dbd7274104e59b5830bf81b8",
    "74fef87580c5353d584a4b424c47fa739b0b3a98839b0494a77087bf1e9966c6",
    "1e7cec942d381bed1d6fb26ba1bed5f9142eea65858fcb18d9a29819a4ac821a",
    "bca5e486b7ba3ca8c711ef3db6b500440603860ae05b4914ed21689443f3cda8",
    "c9e585d8fed30b7275d4b1244d1e0810cfd2593151ed16ac58a1753b49709c23",
    "621c928c7d8722869036cdda8b87077363dc2874aadda409419b66abb43a5148",
]       # Add your togetherAI API keys here


together.api_key = keys[0]
model_list = [d['id'] for d in together.Models.list()]
cnt = 0


def call(prompt, model_ckpt, max_tokens, temperature, top_k, top_p, stop):
    global cnt
    assert model_ckpt in model_list, f"model should be one of {model_list}"

    together.api_key = keys[cnt % len(keys)]
    response = together.Complete.create(
        prompt=prompt,
        model=model_ckpt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        # api_key=keys[cnt % len(keys)],
        stop=stop
    )
    cnt = (cnt + 1) % len(keys)
    # return text
    # return response['output']['choices'][0]['text']
    return response['choices'][0]['text']


def call_TogetherAI(prompt, model_ckpt, max_tokens=256, temperature=0.8, top_k=40, top_p=0.95, stop=None):
    output = None
    while output is None:
        try:
            output = call(prompt, model_ckpt, max_tokens, temperature, top_k, top_p, stop=["\n", "\n\n"])
        except Exception as e:
            print(e)
            print("TogetherAI call failed. Sleeping...")
            time.sleep(1)

    return output


def _test():
    output = call_TogetherAI(
        prompt="<human>: What are Isaac Asimov's Three Laws of Robotics?\n<bot>:",
        model_ckpt="togethercomputer/llama-2-7b",
        max_tokens=256,
        temperature=0.8,
        top_k=60,
        top_p=0.6,
        stop=['<human>', '\n\n']
    )
    print(output)


if __name__ == "__main__":
    print(model_list)
    _test()
