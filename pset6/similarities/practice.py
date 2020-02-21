# edit distance algorithm
a = "sun"
b = "satur"

m = len(a)
n = len(b)
matrix = [[(0,None) for i in range(n+1)] for j in range(m+1)]

for i in range(m + 1):
    for j in range(n + 1):
        if i == 0 and j == 0:
            matrix[i][j] = (0,None)
        elif i == 0:
            matrix[i][j] = (j, "I")
        elif j == 0:
            matrix[i][j] = (i, "D")
        elif a[i-1] == b[j-1]:
            matrix[i][j] = matrix[i-1][j-1]

        else:


            small = 1 + min(matrix[i][j-1][0],matrix[i-1][j][0],matrix[i-1][j-1][0])
            if small == matrix[i][j-1][0]:
                matrix[i][j] = (small,"SS")
            elif small == matrix[i-1][j][0]:
                matrix[i][j] = (small , "Dd")
            elif small == matrix[i-1][j-1][0]:
                matrix[i][j] = (small,"II")
print(matrix[m][n])

