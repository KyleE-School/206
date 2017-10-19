import re
hand = open('HW5_text.txt')
x=list()
for line in hand:
    y=re.findall('[0-9]+',line)
    x=x+y
sum=0
for i in x:
    sum=sum + int(i)
print(sum)