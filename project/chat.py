from main import chat
while True:
    n=chat(input(">"),ai=False)
    print(n["read"],"==>",n["result"])