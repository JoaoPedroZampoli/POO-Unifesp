from datetime import datetime
import random

today = datetime.today().weekday

if today == "Saturday":
    print("Party!")
elif today == "Sunday":
    print("Recover")
else:
    print("Work")

def function(p1, p2 = 10):
    print(p1)
    print(p2)

for i in range(0, 5, 2):
    variavel = random.randint(0, 60)
    function(variavel)