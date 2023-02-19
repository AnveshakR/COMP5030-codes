# Suppose that we have a set of activities to schedule among a large number of lecture halls, 
# where any activity can take place in any lecture hall. We wish to schedule all the activities using as few lecture halls as possible. 
# Devise an efficient greedy algorithm to determine which activity should use which lecture hall and implement it in Python. 
# For driver code, you may generate at random n = 100 activities for a given day during business hours starting at 8 am and ending at 9:30 pm, 
# where each activity lasts from 1 hour to 3 hours with a 30-minute increment; and m = 10 lecture halls.

import random
import numpy as np

def activity_assign(n, hallways, starting_time, ending_time): # takes number of activities and lecture halls
    activities = []
    
    for i in range(n): # generate random activities
        start_interval = random.randint(starting_time, ending_time-2)
        end_interval = random.randint(start_interval + 2, (start_interval + 6) if (start_interval+6) < (ending_time) else (ending_time))
        activities.append((start_interval, end_interval))
    
    graph = np.zeros((n, n))
    
    for i in range(len(activities)): # add activities to graph
        for j in range(len(activities)):
            if i != j:
                for time in activities[i]:
                    start = activities[j][0]
                    end = activities[j][1]
                    if start < time < end:
                        graph[i][j] = 1

    hall_assignment = {}
    colors = [x for x in range(hallways)]
       
    #collects the colors for the neighbor nodes
    for i in range(len(activities)):
        neighbor_colors = []
        for j in range(len(graph[i])):
            if graph[i][j] == 1:
                if j in hall_assignment:
                    neighbor_colors.append(hall_assignment[j])
                    
        #adds nodes not used by neighbors         
        if i not in hall_assignment:
            for color in colors:
                if color not in neighbor_colors:
                    hall_assignment[i] = color
                    break

    minimum_halls = 0
    for _ in range(len(activities)):
        minimum_halls = max(minimum_halls, hall_assignment[i])

    return hall_assignment, minimum_halls


#Driver code
hall_assignment, minimum_halls = activity_assign(hallways = 10, n = 100, starting_time = 0, ending_time = 27) # 27 is the number of 30 minute intervals between 8AM and 9:30PM

print("Minimum number of halls needed is: ", (minimum_halls+1), "\n")

for i in hall_assignment:
    print("activity:",i," lecture hall:", hall_assignment[i])