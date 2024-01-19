import regex as re

def SmallestLessFive(params):
    # change to str so that the indexing is proccess
    if type(params) == int:
        params = str(params)
        
    if len(params) % 2 != 1:
        params = [params[i: i+3] for i in range(0, len(params), 2)]
    else:
        params = [params[i: 4] for i in range(0, len(params), len(params) - 1)]
    
    if '' in params:
        checkIndex = params.index('')
        params.pop(checkIndex)
    
    params = min(list(map(lambda x: int(x), params)))

    return params

    

printOut_1 = SmallestLessFive(5005) 
print(printOut_1) #5

printOut_2 = SmallestLessFive(12345)
print(printOut_2) #12345