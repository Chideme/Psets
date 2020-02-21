# edit distance algorithm
a = "cat"
b = ""

m = len(a)
n = len(b)
l = [[0 for i in range(n+1)] for j in range(m+1)]

for i in range(m + 1):
    for j in range(n + 1):
        if i == 0 and j == 0:
            l[i][j] = (0,"None")
        elif i == 0:
            l[i][j] = (j, "I")
        elif j == 0:
            l[i][j] = (i, "D")
            print(l[i][j][0])
        elif a[-1] == b[-1]:
            l[i][j] = l[i-1][j-1]

