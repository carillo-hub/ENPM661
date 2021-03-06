
#!/usr/bin/python3

import numpy as np
import cv2
import sys
import datetime

starttime = datetime.datetime.now()

#############################################################################################
#Initial / Final State Info  ********TESTER INPUT NEEDED HERE FOR START/GOAL POINTS**********
#############################################################################################

#TestCaseXY = [180,220]
#Plot dimensions
global yscale
global xscale
yscale = 300   
xscale = 400  

#Test Case Initial State:  [x,y] format
#Get pixel x,y coordinates of initial state
TestCaseXY = [399,145]   #<--------------------------TESTER PUT INITIAL X,Y COORDINATE PT HERE
# y = rows.... row 0 = y 300
# v = cols.... col 0 = x 0 
y = yscale - TestCaseXY[1]
x = TestCaseXY[0] 
initial_state = [x, y]  #pixel coors
initial_stateID = tuple(initial_state)
print("Test Case (x,y) starting point is: \n", TestCaseXY, file=open("NodePath.txt", "w"))

#Test Case Final State:  [x,y] format
FinalStateXY = [50, 50]  #<--------------------------TESTER PUT GOAL X,Y COORDINATE PT HERE
y = yscale - FinalStateXY[1]
x = FinalStateXY[0] 
FinalState = [x, y]                                                             #x, y pixel coordinates

global FinalStateID
FinalStateID = tuple(FinalState)    #pixel coors                                #will be referenced for checking if it reached the goal

print("Final state node (x,y): ", FinalStateID)
print("\nTest Case (x,y) goal point is: \n",FinalStateXY, "\n\nThe nodes are stored as a tuple of (x,y) PIXEL coordinates, i.e. the Final State node is ", FinalStateID, file=open("NodePath.txt", "a"))




# Initialize Visited Dictionary
VisitedDict = {}



#############################################################################################
#Video writer info
#############################################################################################

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 2000
outputVideo = cv2.VideoWriter("Sweeping.mp4", fourcc, fps, (xscale, yscale))                #output resolution must match input frame (60% resized from 1980x1020)
print("\n...Creating Video...\n")




#############################################################################################
#Plot -- READS PIXEL COORS and plots pixel coors 
#############################################################################################

def space(CurrentNode, mask, color):
    global FinalState   #PIXEL COORS
    global initial_state  #pixel coors
    
    #Always draw in Obstacle shapes
    cv2.circle(mask, (90, yscale - 70), 35, (128, 255, 0), 2)
    cv2.ellipse(mask, (246,yscale-145), (60,30), 0, 0 , 360, (128,255,0), 2) 
    rect = np.array([[ [48,yscale-108],[36,yscale-125],[159,yscale-211],[171,yscale-194] ]], np.int32) 
    C_shape = np.array([[ [200,yscale-280], [230,yscale-280], [230,yscale-270], [210,yscale-270], [210,yscale-240], [230,yscale-240], [230,yscale-230], [200,yscale-230] ]], np.int32) 
    big_poly = np.array([[ [328,yscale-63], [285,yscale-105], [325,yscale-145], [354,yscale-138], [381,yscale-171], [381,yscale-116] ]], np.int32)
    cv2.polylines(mask, rect, True, (0,255,0),2)
    cv2.polylines(mask, C_shape, True, (0,255,0) ,2) 
    cv2.polylines(mask, big_poly, True, (0,255,0), 2)
    
    #Always draw in Initial/Final State points
    cv2.circle(mask, (FinalState[0],FinalState[1]), 1, (255,0,0), 5)
    cv2.circle(mask, (initial_state[0],initial_state[1]), 1, (255,0,0), 5)
    
    #Draw in Current Node points -- NEEDS PIXEL COORS
    cv2.circle(mask, (CurrentNode[0],CurrentNode[1]), 1, color, 1)
    
    return mask



#############################################################################################
# Queue method
#############################################################################################
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


VisitedQ = Queue()                                                              #Initialize the visited QUEUE --will store the node matrices 


#############################################################################################
# Define boundaries and obstacles (reads nodes as XY coods, checks if in obstacles PIXEL coordinates)
#############################################################################################


def out_of_bounds(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]
    
    if x > xscale or y > yscale or x < 0 or y < 0:
        return True
    else:
        return False

def in_circle(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]
    r = 35
    
    #if inside circle, return true
    if (x -90)**2 + (y-(yscale-70))**2 <= r**2 :
        return True
    else:
        return False
    
def in_oval(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]
    a = 60
    b = 30
    
    #if inside oval, return true
    if ((x -246)**2)/(a**2) + ((y-(yscale-145))**2)/(b**2) <= 1 :
        return True
    else:
        return False

def in_rectangle(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]

    x1 = 48
    y1 = yscale-108
    x2 = 36
    y2 = yscale-125
    x3 = 159
    y3 = yscale-211
    x4 = 171
    y4 = yscale-194
       
    
    #fit 4 lines to make up the rectangle
    #polyfit returns slope and y-int coeff's for linear polynomal
    Mb_1 = np.polyfit([x1, x2],[y1,y2],1)
    Mb_2 = np.polyfit([x2, x3],[y2,y3],1)
    Mb_3 = np.polyfit([x3, x4],[y3,y4],1)
    Mb_4 = np.polyfit([x4, x1],[y4,y1],1)

    #find where Node is in relation to each side of rectangle
    side1 = y - (Mb_1[0] * x) - Mb_1[1]
    side2 = y - (Mb_2[0] * x) - Mb_2[1]
    side3 = y - (Mb_3[0] * x) - Mb_3[1]
    side4 = y - (Mb_4[0] * x) - Mb_4[1]

    #if inside rectangle, return trus
    if side1 <=0 and side2 >=0 and side3 >=0 and side4 <=0:
        return True
    else:
        return False

def in_C_shape1(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]

    x1 = 200
    y1 = yscale-280
    x2 = 230
    y2 = yscale-280
    x3 = 230
    y3 = yscale-270
    x4 = 200
    y4 = yscale-270      
    
    #fit 4 lines to make up the rectangle
    #polyfit returns slope and y-int coeff's for linear polynomal
    Mb_1 = np.polyfit([x1, x2],[y1,y2],1)
    Mb_3 = np.polyfit([x3, x4],[y3,y4],1)

    #find where Node is in relation to each side of rectangle
    side1 = y - (Mb_1[0] * x) - Mb_1[1]
    side3 = y - (Mb_3[0] * x) - Mb_3[1]


    #if inside rectangle, return trus
    if side1 >=0 and x >= x1 and side3 <=0 and x <= x2:
        return True
    else:
        return False

def in_C_shape2(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]

    x1 = 200
    y1 = yscale-270
    x2 = 210
    y2 = yscale-270
    x3 = 210
    y3 = yscale-240
    x4 = 200
    y4 = yscale-240       
    
    #fit 4 lines to make up the rectangle
    #polyfit returns slope and y-int coeff's for linear polynomal
    Mb_1 = np.polyfit([x1, x2],[y1,y2],1)
    Mb_3 = np.polyfit([x3, x4],[y3,y4],1)

    #find where Node is in relation to each side of rectangle
    side1 = y - (Mb_1[0] * x) - Mb_1[1]
    side3 = y - (Mb_3[0] * x) - Mb_3[1]

    #if inside rectangle, return trus
    if side1 >=0 and x >= x1 and side3 <=0 and x <= x2:
        return True
    else:
        return False

def in_C_shape3(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]

    x1 = 200
    y1 = yscale-240
    x2 = 230
    y2 = yscale-240
    x3 = 230
    y3 = yscale-230
    x4 = 200
    y4 = yscale-230       
    
    #fit 4 lines to make up the rectangle
    #polyfit returns slope and y-int coeff's for linear polynomal
    Mb_1 = np.polyfit([x1, x2],[y1,y2],1)
    Mb_3 = np.polyfit([x3, x4],[y3,y4],1)

    #find where Node is in relation to each side of rectangle
    side1 = y - (Mb_1[0] * x) - Mb_1[1]
    side3 = y - (Mb_3[0] * x) - Mb_3[1]

    #if inside rectangle, return trus.
    if side1 >=0 and x >= x1 and side3 <=0 and x <= x2:
        return True
    else:
        return False

def in_poly(Node):
    global xscale
    global yscale
    x = Node[0]
    y = Node[1]

    x1 = 328
    y1 = yscale-63
    x2 = 285
    y2 = yscale-105
    x3 = 325
    y3 = yscale-145
    x4 = 354
    y4 = yscale-138       
    x5 = 381
    y5 = yscale-171
    x6 = 381
    y6 = yscale-116    
    
    #fit 4 lines to make up the rectangle
    #polyfit returns slope and y-int coeff's for linear polynomal
    Mb_1 = np.polyfit([x1, x2],[y1,y2],1)
    Mb_2 = np.polyfit([x2, x3],[y2,y3],1)
    Mb_3 = np.polyfit([x3, x4],[y3,y4],1)
    Mb_4 = np.polyfit([x4, x5],[y4,y5],1)
    Mb_6 = np.polyfit([x6, x1],[y6,y1],1)
    Mb_CUT = np.polyfit([x4, x6],[y4,y6],1)


    #find where Node is in relation to each side of rectangle
    side1 = y - (Mb_1[0] * x) - Mb_1[1]
    side2 = y - (Mb_2[0] * x) - Mb_2[1]
    side3 = y - (Mb_3[0] * x) - Mb_3[1]
    side4 = y - (Mb_4[0] * x) - Mb_4[1]
    side6 = y - (Mb_6[0] * x) - Mb_6[1]
    sideCUT = y - (Mb_CUT[0] * x) - Mb_CUT[1]

    #if inside rectangle, return trus.
    if side1 <=0 and side2 >=0 and side3 >=0 and side6 <=0 and sideCUT >=0:
        return True
    if side4 >=0 and x <= x5 and sideCUT <=0:
        return True
    
    
    else:
        return False
        
def in_obstacles(Node):
    in_rect = in_rectangle(Node) 
    in_ovl = in_oval(Node)
    in_circ = in_circle(Node)
    in_C1 = in_C_shape1(Node)
    in_C2 = in_C_shape2(Node)
    in_C3 = in_C_shape3(Node)
    in_big_poly = in_poly(Node)
    out_of_bound = out_of_bounds(Node)

    if in_rect  == True or in_ovl == True or in_circ == True or in_C1 == True or in_C2 == True or in_C3 == True or in_big_poly == True or out_of_bound == True:
        return True
    else:
        return False



#############################################################################################
# Verify Initial/Goal state are in boundaries and out of obstacles, Initialize the Plot
#############################################################################################
    
#TRUE = failed obstacle check
obstacles_check_GOAL = in_obstacles(FinalState)
obstacles_check_INITIAL = in_obstacles(initial_state)

if obstacles_check_GOAL == True:                                                #impose constraint
    print("\nfinal state IN an obstacle -- choose another please\n")
    sys.exit()

if obstacles_check_INITIAL == True:                                             #impose constraint
    print("\ninitial state IN an obstacle -- choose another please\n")
    sys.exit()


#Initialize the plot in the video frame sequence
global mask
mask = 255*np.ones((300, 400, 3), np.uint8)                                     #mask to plot on
mask = space(initial_state, mask, (0,0,0))                                      #initialize the plot
outputVideo.write(mask)                                                         #output frame to video sequence


#############################################################################################
# Plot the Optimal Path -- PLOTTING IN PIXEL COORS
#############################################################################################

def Plot_OurMap(OurMap):
    
    global mask

    for EachID in OurMap:
        x = int(EachID[0])
        y = int(EachID[1])
        CurrentNode = [x, y]


        mask = space(CurrentNode, mask, (255,0,0))
        outputVideo.write(mask)


    #Video compelte, calculate code run time
    outputVideo.release()
    endtime = datetime.datetime.now()
    runtime = endtime - starttime
    print("\nRun time: ", runtime)

    print("\nDone. Can see results in NodePath.txt and Sweeping.mp4!")
    sys.exit()


#############################################################################################
# Define parent/child roadmap for initial state to goal state --MAP IS PIXEL COORS
#############################################################################################

def roadmap(ID):
    
    global parent_index

    OurMap = []                                                                 #initialize the roadmap
    OurMap.append(ID)                                                           #start by adding final state tuple
    parent = VisitedDict[ID]                                                    #get parent tuple
    ID = parent                                                                 #set parent -> new child
        
    while parent != 'Initial State':
        OurMap.append(ID)                                                       #add child tuple to road map
        parent = VisitedDict[ID]                                                #get parent tuple
        ID = parent                                                             #set parent -> new child
            
        if parent == 'Initial State': 
            OurMap.reverse()                                                    #pitstops were grabbed in reverse order (Goal --> Initial), so need to reverse
            break 
        
    print("\nOur Road Map is: ",OurMap , file=open("NodePath.txt", "a"))
    
    Plot_OurMap(OurMap)

     
 
#############################################################################################
# Define 4 functions to move the blank tile in each direction and store the NewNode in a list
############################################################################################# 

def CheckAction(NewNode):
    
    global FinalStateID
    ID = tuple(NewNode)                                                         #get the tuple of child node
        
    if ID == FinalStateID:                                                      #check if child node == final node
        
        print("\nThis Game Over \n Final State Node: \n", NewNode, file=open("NodePath.txt", "a"))
        
        VisitedDict[ID] = parent_index                                          #answer YES, so add to visited dict
        roadmap(ID)                                                             #compute the roadmap from initial to final state
    
    else: 

        if ID in VisitedDict:                                                   #Check if ID was visited
            pass                                                                #answer YES, so move on
        if ID not in VisitedDict:                                               #answer NO, so this is a child --add to Q
            VisitedQ.enqueue(NewNode)                                           #add to Q
            VisitedDict[ID] = parent_index                                      #add to visited coupled with parent
            
def MoveUp(NewNode):
    x, y = NewNode                                                             #check the action                           #array value at the blank ("0")
    swap1 = [x, y-1]                                                           #perform the action                     #array value to left of blank 
    NewNode = swap1                         
    CheckAction(NewNode)                                                       #check the action
def MoveUpRight(NewNode):
    x, y = NewNode                                                             #check the action                            #array value at the blank ("0")
    swap1 = [x+1, y-1]                                                         #perform the action  
    NewNode = swap1                       
    CheckAction(NewNode)                                                        #check the action
def MoveRight(NewNode):
    x, y = NewNode                                                             #check the action                           #array value at the blank ("0")
    swap1 = [x+1, y]                                                            #perform the action
    NewNode = swap1                        
    CheckAction(NewNode)                                                        #check the action
def MoveDownRight(NewNode):
    x, y = NewNode                                                             #check the action
    swap1 = [x+1, y+1]                                                         #perform the action
    NewNode = swap1                    
    CheckAction(NewNode)                                                       #check the action
def MoveDown(NewNode):
    x, y = NewNode                                                             #check the action
    swap1 = [x, y+1]                                                           #perform the action
    NewNode = swap1                         
    CheckAction(NewNode)                                                       #check the action
def MoveDownLeft(NewNode):
    x, y = NewNode                                                              #check the action
    swap1 = [x-1, y+1]                                                          #perform the action
    NewNode = swap1                         
    CheckAction(NewNode)                                                        #check the action
def MoveLeft(NewNode):
    x, y = NewNode                                                              #check the action
    swap1 = [x-1, y]                                                            #perform the action
    NewNode = swap1                        
    CheckAction(NewNode)                                                        #check the action
def MoveUpLeft(NewNode):
    x, y = NewNode                                                              #unpack the node into pixel x y coords               
    swap1 = [x-1, y-1]                                                          #perform the action
    NewNode = swap1                          
    CheckAction(NewNode)                                                        #check the action

def ActionSet(CurrentNode):
    
    global x
    global y
    global mask
    NewNode = CurrentNode.copy()

    #TRUE = failed obstacle check
    obstacles_check = in_obstacles(CurrentNode)
    if obstacles_check == True:                                                 #impose constraint
        return CurrentNode
    
    else:                                                        
        mask = space(CurrentNode, mask, (0,0,255))                              #add validated parent node to output video
        outputVideo.write(mask)
  
    MoveUp(NewNode)                                                             #perform action set
    MoveUpRight(NewNode)
    MoveRight(NewNode)
    MoveDownRight(NewNode)
    MoveDown(NewNode)
    MoveDownLeft(NewNode)
    MoveLeft(NewNode)
    MoveUpLeft(NewNode)  


#############################################################################################
# Follow the flow chart
#############################################################################################

initial_stateID = tuple(initial_state)                                           #tuple pixel coors
print("\nInitial State node  ", initial_stateID)
VisitedDict[initial_stateID] = 'Initial State'                                   #add initial state into Visited Data Structure

VisitedQ.enqueue(initial_state)                                                  #add initial state into Q
Checkit = 0
ID = tuple(initial_state)                                                        #tuple pixel coors

while ID != FinalStateID:                                                        #pixel coors check if current node == final state                                                    #While loop until FinalState is reached

    Checkit = VisitedQ.dequeue()                                                 #answer NO, so remove FIFO node from Q and store in a variable
    ID = tuple(Checkit)                                                          #tuple pixel coors                                                   #Get the tuple value of the node in variable
    parent_index = ID                                                            #Make node a parent
    ActionSet(Checkit)                                                           #Get the children





