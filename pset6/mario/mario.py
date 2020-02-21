
#prompt for height
#height range
height_range = [i for i in range(24)]

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))
    except ValueError:
       print("Please enter an integer")
       continue
    else:
       return userInput
       break


height = inputNumber("Please enter an integer: ")
while height not in height_range:
    height = inputNumber("Please enter an integer: ")
i = 0
space = " "
hash_ = "#"
for i in range(0, height):
    #number of spaces
    n = height - (i + 1)
    #number of hashes
    p = i + 2
    print("{:s}{:s}".format(space * n, hash_ * p))
