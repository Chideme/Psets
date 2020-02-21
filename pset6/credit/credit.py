# prompt for user input
def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))
    except ValueError:
       continue
    else:
       return userInput
       break
number = inputNumber("Number: ")
number = str(number)
num_list = [int(number[i]) for i in range(0,len(number))]
num_list.reverse()
left = [num_list[i] for i in range(0,len(num_list),2)]
sec = [(num_list[i]  *2)for i in range(1,len(num_list),2)]
s = ""
for i in sec:
    s += str(i)
d = 0
for i in s:
    d += int(i)
total = d + sum(left)

if total % 10 == 0:
    if number[:2] in ["51","52","53","54","55"]:
        print("MASTERCARD\n")
    elif number[:2] in ["34","37"] and len(number) == 15:
        print("AMEX\n")
    elif number[0] == "4" and len(number) == 13  or number[0] == "4" and len(number) == 16:
        print("VISA\n")
    else:
        print("INVALID\n")
else:
    print("INVALID\n")




