raw = "{'coulmn_type': 'natural language text', 'reason': 'The 'address' column contains ...'}"
def eval_result(text:str):
    try:
        return eval(text)
    except:
        ratextw = text.strip(" {}")
        parts = ratextw.split("', '")
        res = {}
        for part in parts:
            key, value = part.split(": '")
            res[key.strip("'")] = value.strip("'")
        return res
    
print(eval_result(raw))