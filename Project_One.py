
#!/usr/bin/python3

import numpy as np
import sys
import argparse
import os

#os.remove("NodePath.txt")

parser = argparse.ArgumentParser()
parser.add_argument('--testcase', type=str,default='TestCase1',required=False)
args = parser.parse_args()

#Test Case Initial State
TestCase1 = [[1, 2, 3, 4],[ 5, 6, 0, 8], [9, 10, 7, 12] , [13, 14, 11, 15]]
TestCase2 = [[1, 0, 3, 4],[ 5, 2, 7, 8], [9, 6, 10, 11] , [13, 14, 15, 12]]
TestCase3 = [[0, 2, 3, 4],[ 1, 5, 7, 8], [9, 6, 11, 12] , [13, 10, 14, 15]]
TestCase4 = [[5, 1, 2, 3],[ 0, 6, 7, 4], [9, 10, 11, 8] , [13, 14, 15, 12]]
TestCase5 = [[1, 6, 2, 3],[ 9, 5, 7, 4], [0, 10, 11, 8] , [13, 14, 15, 12]]

if args.testcase == "TestCase1" :
    initial_state = np.array(TestCase1)
elif args.testcase == "TestCase2" :
    initial_state = np.array(TestCase2)
elif args.testcase == "TestCase3" :
    initial_state = np.array(TestCase3)
elif args.testcase == "TestCase4" :
    initial_state = np.array(TestCase4)
elif args.testcase == "TestCase5" :
    initial_state = np.array(TestCase5)
else: 
    sys.exit("Choose a valid TestCase1-5") 

print("Test Case is: \n", initial_state, file=open("NodePath.txt", "w"))


# Initialize Currentnode, NewNode, and index
CurrentNode = initial_state                     #4x4 array 
NewNode = None
index = 0                                       #will e used to track number of moves, and the parent index
childparent = []                                #Initialize the parent/child list

#######################################################################################################
# Queue method
#######################################################################################################
class Queue:
    
    def __init__(Visited):
        Visited.items = []                       #This is our Visited list
        
    def enqueue(Visited,item):                   #Adding items to Visited
        Visited.items.insert(0,item)
    
    def size(Visited):                           #Determine length of Visited
        return len(Visited.items)

    def dequeue(Visited):                        #Deleting items from Visited
        if Visited.items:
            return Visited.items.pop()
        else:
            return None 


Visited = Queue()                               #Initialize the visited QUEUE --will store the node matrices 
Visited_list = []                               #Initialize the visited LIST --easily searchable, will hold the string node IDs
       
############################################################################
# Define concatenation and Node state IDs 
############################################################################
def concat(a, b):                               #function to concat matrix to a string ID
    return str(f"{a}{b}")                       #source: https://www.askpython.com/python/string/python-concatenate-string-and-int

def string(Node):
    string2 = str(0)                            #This will be used for very first concat (needs something to concat to). AKA all IDs will start with a "0"
    for x in range(0,4):                        
        for y in range(0,4):
            string1 = str(Node[x,y])            #Scan Node array, find each point 
            if len(string1) == 1:               #If point is 1 digit, add 0 in front
                string1 = concat("0",string1)
            concated = concat(string2,string1)  #Concat each point to the last 
            string2 = concated                  #Set new object to concat to until you've gone through entire Node array
    return concated


#Goal State
FinalState = np.array([[1, 2, 3, 4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
FinalStateID = string(FinalState)

print("The nodes are stored row-wise, i.e. the Final State node is stored as ", FinalStateID," and these IDs all start with a 0", file=open("NodePath.txt", "a"))

############################################################################
# Define parent/child roadmap for initial state to goal state
############################################################################

def roadmap(childparent):
    
    global parent_index
    global initial_state
    nextone = None 
    start = childparent[parent_index]           #Start with the goal state
    Initial = string(initial_state)             #Get goal state string ID
    OurMap = []                                 #Initialize the RoadMap list
        
    while nextone != 'Initial State':           #Do this loop until we reach the Initial State
       
        nextone = start[0]                      #Identify the next parent's index number
        thisstop = start[1]                     #Identify the parent's child ID string
        OurMap.append(thisstop)                 #add the child ID string to the roadmap as one of the "pitstops"
        if nextone == 'Initial State':          #once the "initial state" is the parent index, we're done
            break
        start = childparent[nextone]            #for each stop (nextone) keep grabbing the next parent/child until reach the initial state
    
    OurMap.reverse()                            #pitstops have been grabbed in reverse order (Goal --> Initial), so need to reverse it back
    OurMap.append(FinalStateID)                 #the while loop started with the final state's parent as the child, so need to add the finalstate ID to the map
    print("Our Road Map is: ",OurMap , file=open("NodePath.txt", "a"))
    print("Visited list (explored nodes) is from start node to goal node is: \n",Visited_list,  file=open("NodePath.txt", "a"))
    sys.exit()
    
#############################################################################################
# Define 4 functions to move the blank tile in each direction and store the NewNode in a list
#############################################################################################
    
def ActionMoveDown(CurrentNode):
    global u
    global v
    global index 
    NewNode = CurrentNode.copy()

    if u == 3:                                      #impose constraint
        return CurrentNode
    
    else:                                           #perform the tile swap
        
        blank = NewNode[u,v]                        #array value at the blank --> ("0")
        swap1 = NewNode[u+1,v]                      #array value below blank 
        NewNode[u,v] = swap1                        #make the blank tile now equal the swap value
        NewNode[u+1,v] = blank                      #make the swap tile now equal  the blank value
        swap1 = NewNode[u,v]                        #cross check to make sure the newly swapped tile is now a free number 
        blank = NewNode[u+1,v]                      #cross check to make sure the new blank is now actually a blank
        
        
        ID = string(NewNode)                        #get the string value of child node
        
        if ID == FinalStateID:
            print("This Game Over \n Final State: \n", NewNode, "\n How Many Moves (explored nodes): ",index , file=open("NodePath.txt", "a"))
            it = (parent_index,ID)                  #grab the parent index number and the child node's ID
            childparent.append(it)                  #and add it to the childparent list
            roadmap(childparent)                    #compute the roadmap from initial to final state
             
        else: 
            Visited.enqueue(NewNode)                #put child node into stack

            if ID in Visited_list:                  #quick check to see if the new node is already in the Visited ID list
                pass                                #answer YES, so move on
            if ID not in Visited_list:              #answer NO, so this is a "good" child --add it to the childparent list
                config_num = index                  #identify this node's index number
                it = (parent_index,ID)              #grab the parent index number and the child node's ID
                childparent.append(it)              #and add it to the childparent list
        return NewNode                              #makes sure the function output is assigned to "NewNodeX
 

def ActionMoveUp(CurrentNode):
    global u
    global v
    global index 
    NewNode = CurrentNode.copy()

    if u == 0:                                      #impose constraint
        return CurrentNode

    else:                                           #perform the tile swap
        
        blank = NewNode[u,v]                        #array value at the blank --> ("0") 
        swap1 = NewNode[u-1,v]                      #array value above blank 
        NewNode[u,v] = swap1                        #make the blank tile now equal the swap value
        NewNode[u-1,v] = blank                      #make the swap tile now equal  the blank value
        swap1 = NewNode[u,v]                        #cross check to make sure the newly swapped tile is now a free number
        blank = NewNode[u-1,v]                      #cross check to make sure the new blank is now actually a blank
        
        ID = string(NewNode)                        #get the string value of child node
        
        if ID == FinalStateID:
            print("This Game Over \n Final State: \n", NewNode, "\n How Many Moves (explored nodes): ",index, file=open("NodePath.txt", "a"))
            it = (parent_index,ID)                  #grab the parent index number and the child node's ID
            childparent.append(it)                  #and add it to the childparent list
            roadmap(childparent)                    #compute the roadmap from initial to final state
            
       
        else: 
            Visited.enqueue(NewNode)                #put child node into stack

            if ID in Visited_list:                  #quick check to see if the new node is already in the Visited ID list
                pass                                #answer YES, so move on
            if ID not in Visited_list:              #answer NO, so this is a "good" child --add it to the childparent list
                config_num = index                  #identify this node's index number
                it = (parent_index,ID)              #grab the parent index number and the child node's ID
                childparent.append(it)              #and add it to the childparent list
        return NewNode                              #makes sure the function output is assigned to "NewNodeX
  

def ActionMoveRight(CurrentNode):
    global u
    global v
    global index 
    NewNode = CurrentNode.copy()

    if v == 3:                                      #impose constraint
        return CurrentNode 
    
    else:                                           #perform the tile swap

        blank = NewNode[u,v]                        #array value at the blank --> ("0")
        swap1 = NewNode[u,v+1]                      #array value to right of blank      
        NewNode[u,v] = swap1                        #make the blank tile now equal the swap value
        NewNode[u,v+1] = blank                      #make the swap tile now equal  the blank value
        swap1 = NewNode[u,v]                        #cross check to make sure the newly swapped tile is now a free number   
        blank = NewNode[u,v+1]                      #cross check to make sure the new blank is now actually a blank
        
    
        ID = string(NewNode)                        #get the string value of child node
        
        if ID == FinalStateID:
            print("This Game Over \n Final State: \n", NewNode, "\n How Many Moves (explored nodes): ",index, file=open("NodePath.txt", "a"))
            it = (parent_index,ID)                  #grab the parent index number and the child node's ID
            childparent.append(it)                  #and add it to the childparent list
            roadmap(childparent)                    #compute the roadmap from initial to final state
        
        else: 
            Visited.enqueue(NewNode)                #put child node into stack

            if ID in Visited_list:                  #quick check to see if the new node is already in the Visited ID list
                pass                                #answer YES, so move on
            if ID not in Visited_list:              #answer NO, so this is a "good" child --add it to the childparent list
                config_num = index                  #identify this node's index number
                it = (parent_index,ID)              #grab the parent index number and the child node's ID
                childparent.append(it)              #and add it to the childparent list
        return NewNode                              #makes sure the function output is assigned to "NewNodeX
  

def ActionMoveLeft(CurrentNode):
    global u
    global v
    global index
    NewNode = CurrentNode.copy()

    if v == 0:                                      #impose constraint
        return CurrentNode 
    
    else:                                           #perform the tile swap
        
        blank = NewNode[u,v]                        #array value at the blank ("0")
        swap1 = NewNode[u,v-1]                      #array value to left of blank 
        NewNode[u,v] = swap1                        #make the blank tile now equal the swap value
        NewNode[u,v-1] = blank                      #make the swap tile now equal  the blank value
        swap1 = NewNode[u,v]                        #cross check to make sure the newly swapped tile is now a free number
        blank = NewNode[u,v-1]                      #cross check to make sure the new blank is now actually a blank
        
        ID = string(NewNode)                        #get the string value of child node
        
        if ID == FinalStateID:
            print("This Game Over \n Final State: \n", NewNode, "\n How Many Moves (explored nodes): ",index, file=open("NodePath.txt", "a"))
            it = (parent_index,ID)                  #grab the parent index number and the child node's ID
            childparent.append(it)                  #and add it to the childparent list
            roadmap(childparent)                    #compute the roadmap from initial to final state
        
        else: 
            Visited.enqueue(NewNode)                #put child node into stack

            if ID in Visited_list:                  #quick check to see if the new node is already in the Visited ID list
                pass                                #answer YES, so move on
            if ID not in Visited_list:              #answer NO, so this is a "good" child --add it to the childparent list
                config_num = index                  #identify this node's index number
                it = (parent_index,ID)              #grab the parent index number and the child node's ID
                childparent.append(it)              #and add it to the childparent list
        return NewNode                              #makes sure the function output is assigned to "NewNodeX
 

################################################################################################
# Follow the flow chart
################################################################################################

ID = string(CurrentNode)                        #get the string value of initial state 
start_childparent = ("Initial State",ID)        #Initialize the parent/child list
childparent.append(start_childparent)           #Start the parent/child list with the initial state
Visited.enqueue(CurrentNode)                    #put initial state into stack
Checkit = 0

while ID != FinalStateID:                       #While loop until FinalState is reached
    Checkit = Visited.dequeue()                 #remove first node from front of queue and store in a variable
    ID = string(Checkit)                        #Get the string value of the node in question
    
    while ID in Visited_list:                   #check whether first node is in Visited list 
        Checkit = Visited.dequeue()             #answer YES, so remove the next node from front of queueu and store in a variable
        ID = string(Checkit)                    #Get the string value of the node in question
    
    while ID not in Visited_list:               #check whether first node is NOT in Visited list
        Visited.enqueue(Checkit)                #answer NO, so push the node back into queue and...
        Visited_list.append(ID)                 #add the ID to the Visited list (only non-duplicates get added!! so can never have a duplicate in visited list)
        parent_index = index                    #initialize the parent index number
        index = index + 1
        
        u,v = np.where(Checkit == 0)            #find blank tile 
        init_point = np.array((u,v)).T  
    
        NewNode1 = ActionMoveDown(Checkit)      #perform action and get children (x4)
        NewNode2 = ActionMoveUp(Checkit) 
        NewNode3 = ActionMoveRight(Checkit)         
        NewNode4 = ActionMoveLeft(Checkit)

