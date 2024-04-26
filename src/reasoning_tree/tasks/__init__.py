def get_task(name):
    if name == 'gsm8k':
        from .gsm8k import GSM8kTask
        return GSM8kTask()
    elif name == 'SVAMP':
        from .SVMP import SVMPTask
        return SVMPTask()
    elif name == 'multiarith':
        from .multiarith import multiarithTask
        return multiarithTask()
    else:
        raise NotImplementedError