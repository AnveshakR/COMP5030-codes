# Write a Python program to implement the coin-collecting robot program using dynamic programming on an m x n map. 
# Your program should return a path for the robot to walk through that contains the largest possible number of coins under the following restriction: 
# In a single step, the robot can move at most one cell east, or one cell south, or one cell southwest. 
# The robot can start from any position in the top row, and must stop at the lowerleft corner.

# What's a path the robot should move on the following map and what is the number of coins it collects on the path? 
# In the map, 1 represents there is a coin and 0 otherwise.


import numpy as np

def coin_counter(r,c,input_matrix):
    output_map=[[0]*(c+1) for _ in range(r+1)] # new padded array so that the east and south nodes dont go out of bounds

    # bottom-up approach
    for i in range(1, r+1):
        for j in range(1, c+1):
            try:
                output_map[i][j] = max(output_map[i-1][j], output_map[i][j-1], output_map[i+1][j-1]) + input_matrix[i-1][j-1] # checks for coin in east, south and southwest nodes
            except:
                output_map[i][j] = max(output_map[i-1][j], output_map[i][j-1]) + input_matrix[i-1][j-1] # except block because the southwest node goes out of bounds for some iterations

    print('Maximum Coins Collected: ',output_map[r][c])
    print('Final Path: \n', np.flip(np.matrix(output_map), 1))
    print("The output matrix describes the collection of coins at each level")

input_matrix=[[1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]]

print("Input Matrix: \n", np.matrix(input_matrix))

input_matrix = np.flip(np.matrix(input_matrix), 1).tolist()

coin_counter(len(input_matrix),len(input_matrix[0]),input_matrix)