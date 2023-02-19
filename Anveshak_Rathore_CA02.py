# The class sample code on finding an LCS of two strings returns the rightmost LCS. 
# Modify the class code to return the leftmost LCS of two strings. 
# Let X = AABCCDIEEDSCYBA and Y = ABBCDDEFDHCNBAT. 
# Return the leftmost LCS of X and Y, as well as the rightmost LCS.


from __future__ import print_function

def bottom_up_lcs_path(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
 
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
    P = [[0]*(n + 1) for i in range(m + 1)]
    for i in range(m + 1):
        L[i][0] = 0
    for j in range(n + 1):
        L[0][j] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
                P[i][j] = "upleft"
            elif L[i-1][j] >= L[i][j-1]: 
                L[i][j] = L[i-1][j]
                P[i][j] = "up"
            else:
                L[i][j] = L[i][j-1]
                P[i][j] = "left"
    return L[m][n], P

def print_lcs(P, X, i, j, result):
    if i == 0 or j == 0:
        return
    if P[i][j] == "upleft":
        print_lcs(P, X, i - 1, j - 1, result)
        result.append(X[i-1])
    elif P[i][j] == "up":
        print_lcs(P, X, i - 1, j, result)
    else:
        print_lcs(P, X, i, j - 1, result)

X = "AABCCDIEEDSCYBA"
Y = "ABBCDDEFDHCNBAT"

print("String 1: ", X)
print("String 2: ", Y)

# for LCS from left side

result = []

P = bottom_up_lcs_path(X, Y)[1] # building path for input strings
m = len(X)
n = len(Y)

print_lcs(P, X, m, n, result) # computing LCS
print("LCS from left side: ", *result, sep="")

# for LCS from right side

result = []

P = bottom_up_lcs_path(X[::-1], Y[::-1])[1] # building path for reversed strings
m = len(X)
n = len(Y)

print_lcs(P, X[::-1], m, n, result) # computing LCS
print("LCS from right side: ", *result, sep="")