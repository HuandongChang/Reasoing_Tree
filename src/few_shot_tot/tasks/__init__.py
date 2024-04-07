def get_task(name):
    if name == 'gsm8k':
        from .gsm8k import GSM8kTask
        return GSM8kTask()
    else:
        raise NotImplementedError