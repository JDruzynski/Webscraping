import json

dictPrint = lambda dic : print(json.dumps(dic, ensure_ascii=False, indent=4))

def listPrint(li, spaces:int = 0):
    for l in li:
        if type(l) is dict:
            dictPrint(l)
        else:
            print(l)

        for _ in range(0,spaces): print()
