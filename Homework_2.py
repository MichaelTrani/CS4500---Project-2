# coding=utf-8
"""
Michael Trani
9/11/2019
Introduction to the Software Profession:
CompSci 4500 - 001
Homework 2


The old:
This program plays a circle jumping game, described in section Reference 01.
This UPDATED version has been updated as per specifications described in Reference 02.
The program reads a file to collect the number of circles, the number of routes, and a map of the routes formatted as such: [Source Circle][blank space][Destination Circle]
The program ensures there are not more than twenty circles, and no less than two. 
It also ensures that the number of routes given match the quantity of routes given.
The circles are given their own class containing a list for routes, a dictionary to track the use of routes, a visit count, a boolean to check when the circle has been visited, and a unique ID for troubleshooting.

What's new?
In this UPDATED version: a list, initialRouteList, is added to the circle class.
As the program reads the routes from the infile, it removes recursive routes and performs three tests.
Test 1: Does every circle have a route going in?
Test 2: Does every circle have a route going out?
Test 3: If we search every circle's routes, can we find a path that touches every circle that leads to the initial circle?

Test 3 searches the initialRouteList of every circle to find a path to circle 1. The source of that path, circle n, is stored in the list, Path, then seaches for a route that leads to itself.
As a for loop progresses, it skips circles already added to the path in an attempt to eliminate infinite loops and unnecessary backtracking.

The circle classes are stored in a list for easy access.
The 0th element of the list is populated with a dummy circle for easier bookkeeping.

Once populated, an infinite loop goes through the process described in Reference 01 while being looped 10 times, as described in Reference 02.


#### Reference 01 ####
Imagine there is white board. You draw non-intersecting circles on the board, numbered 1 to N, where N is an integer from 2 to 10. You next draw arrows from one circle to another, making sure that each circle has at least one OUT arrow and one IN arrow. Now you play the following “game:”

Place a magnetic marker in circle #1, and put a check mark in circle #1. The circle where the marker resides is called the “current circle.”
Randomly choose among the out arrows in the current circle. (If there is only one out arrow, that choice is trivial.) In this selection, all the out arrows should be equally likely to be picked.
Move the marker to the circle pointed to by the out arrow. This becomes the new current circle.
Put a check mark in the current circle.
If all the circles have at least one check mark, stop the game. If not, go to step 2 and repeat.
Your first programming assignment is to implement this game. You will use the language Python 3. You may use any IDE that you'd prefer, but you will hand in a ".py" file, not a file that is specialized to any particular IDE. I will be running your program from a command line.  The program will read from a textfile in the same directory as the executable program, and will write to another textfile in that same directory.

Let N and K be positive integers. For HW1, N is between 2 and 10 inclusive.

The input text file should be named HW1infile.txt. It should be in this form:

The first line has only the number N, the number of circles that will be used in your game.
The second line has the number K, the number of arrows you will “drawing” between the circles.
The next K lines designate the arrows, one arrow per line. Each arrow line consists of two numbers, each number being one of circles in the game. These two numbers are separated by a single blank. The first number designates the circle that is the source (back end) of the arrow; the second number designates the circle that is the destination (pointed end) of the arrow.
The circles and arrows of this game describe a directed graph, sometimes known as a “diagraph.” In order to set up the game correctly, you should describe a “strongly connected diagraph” in your input file. A diagraph is strongly connected when there is a path between any two nodes. In our game, our paths are the arrows, and our nodes are circles.

If the text in the input file does not follow the format described above, your program should end with an error message to the screen and to an output file. The output file should be a textfile. Name your output textfile “HW1lastnameOutfile.txt” where “lastname” is replaced by your last name. My output file would be called HW1millerOutfile.txt.

If the text in the input file DOES follow the description above, then you should play the game until each circle has at least one check. When that happens, the game stops. At the end of the game, you should print out to the screen, and to the output textfile, the following numbers:

The number of circles that were used for this game
The number of arrows that were used for this game
The total number of checks on all the circles combined. (Thought question: how is this related to the number of arrows traversed?)
The average number of checks in a circle marked during the game.
The maximum number of checks in any one circle. (NOTE: this number may occur in more than one circle, and that’s fine.)

#### End of Reference 01 ####

#### Reference 02 ####

In HW1, you were to assume that the data in the file HW1infile.txt defined a circles and arrows system that was a strongly connected digraph. That is, there was a path of arrows between any two circles. In HW2, you can’t assume that characteristic of the input circles and arrows. You must TEST that assumption. If the system of circles and arrows IS strongly connected, then your program should continue processing; but if the system is NOT connected, then your program should write an error message to the screen and to the output file that describes the problem, and then halt.
As before, make sure that the input file conforms to the specified format. If the input file deviates from the specified format, print an error message to the screen and to the output file, and halt. In HW2, you may assume that the number of out arrows at any circle will not exceed 20.
The name of the output file for HW2 should be HW2lastnameOutfile.txt where lastname is your last name.
In HW1, you simulated one game of circles and arrows after reading in the file. For HW2, if the input file correctly defines a connected system of circles and arrows, you will do something different. Although you will read in the input file information once (like before), for HW2 you’ll run that simulated game ten (10) times. Before each simulated game, reinitialize to the start of a game. Keep statistics on the 10 game simulations, and then print out to the screen and to the output file the following information:
•	The average number of total checks per game
•	The maximum number of total checks in a single game
•	The minimum number of total checks in a single game
•	The average number of checks on a single circle over all the games
•	The minimum number of single circle checks
•	The maximum number of single circle checks
In HW1, the maximum number of circles was 10. Increase that to 20.
Impose a limit of a million checks on any one game. If that limit is reached, stop the program with a sensible output that helps the user know what happened.




"""
import random


# Circle class to keep track of all node data
class Circles:
    def __init__(self, visited, initialVisited, TimesVisited, Odometer, testID):
        self.visited = visited  # Bool to check if circle has been visited, or "checked"
        self.initialVisited = initialVisited
        self.TimesVisited = TimesVisited  # Integer to track amount of times circle has been "checked"
        self.Odometer = {}  # Dictionary to keep track of which routes, of "arrows" have been used
        self.RouteList = []  # List of routes, or "arrows"
        self.initialRouteList = []
        self.testID = testID  # Unique ID, or serial number


gameRounds = 10

# Get amount of circles and routes from infile, create List of Circles. Create output file.
inFile = open('HW2infile.txt', 'r')
outFile = open('HW2traniOutfile.txt', 'w')

# Check Circle Count
CircleCount = int(inFile.readline())
if (CircleCount > 20 or CircleCount < 2):
    print("Circle count out of bounds from input file.")
    outFile.write("Circle count out of bounds from input file.")
    exit()

routeCount = int(inFile.readline())  # Obtain number of routes, or "arrows"
CircleSet = []  # List of Circle objects

# Create empty Circle for easier bookkeeping:
CircleSet.append(Circles(bool(True), bool(True), 0, [], ("testID: EMPTY CIRCLE")))

# Circle List Constructor
for i in range(1, CircleCount + 1):
    CircleSet.append(Circles(bool(False), bool(False), int(0), [], ("testID: ", i)))
# print (CircleSet[i].testID)


# Route Populator reads inFile to obtain source and destination routes
# Populates a list in the Circle Class and Creates an Odometer for each route in a dictionary.

MasterOdometer = 0  # Used for counting route maps
routeCheckerIn = []  # used to check that every circle receives a route
circleCheckerOut = []  # used to check that every circle has an exit route

for line in inFile:
    circle, destination = line.split()
    circle = int(circle)
    destination = int(destination)

    if destination != circle:  # Reduce calculations counts for strength test
        CircleSet[circle].initialRouteList.append(destination)
        routeCheckerIn.append(int(destination))
        circleCheckerOut.append(int(circle))

    CircleSet[circle].RouteList.append(destination)
    CircleSet[circle].Odometer[destination] = 0
    routeCheckerIn.append(int(destination))
    circleCheckerOut.append(int(circle))
    MasterOdometer += 1

if MasterOdometer != routeCount:  # Make sure there is the proper amount of routes
    print("Invalid Route Count in input file.")
    outFile.write("Invalid Route Count in input file.")
    exit()

routeCheckerIn = list(dict.fromkeys(routeCheckerIn))  # remove duplicates
routeCheckerIn.sort()  # sort for checking

# Test 1 - all circles should have incoming routes
if len(routeCheckerIn) < CircleCount:
    print("Soft Test Failed, not all circles reachable")
    outFile.write("Soft Test Failed, not all circles reachable")
    outFile.close()  # Close output file
    exit()

circleCheckerOut = list(dict.fromkeys(circleCheckerOut))  # remove duplicates
circleCheckerOut.sort()  # sort for checking

# Test 2 - all circles should have outgoing routes
if len(circleCheckerOut) < CircleCount:
    print("Soft Test Failed, not all circles travel")
    outFile.write("Soft Test Failed, not all circles travel")
    outFile.close()  # Close output file
    exit()

# Test 3 - Pathfinding test
# This attempts to find a path backwards from the starting point.
# Each circle's non-recursive paths are checked to find the current circle.
# The process is repeated until all circles have been reached
# Weakly connected graphs can create an infinite loop so a million iteration limit is set as an exit condition.

# The finalDestination variable is similar the game marker, it gets updated when a leading route is found.
finalDestination = int(1)
path = [finalDestination]  # The path list collects the circles visited
pathCounter = 0  # Iteration counter for stop control.

while len(path) < CircleCount:  # This should stop the cycle when all circles have been reached.
    pathCounter += 1

    for i in range(1, CircleCount + 1):  # This is the circle in which you're looking for routes.
        if i in path:  # Check circles already used and skip them to prevent entering an infinite loop
            continue

        # Searches the list of non-recursive routes in a circle, looking for the route that leads to the current circle
        for k in range(0, len(CircleSet[i].initialRouteList)):

            if CircleSet[i].initialRouteList[k] == finalDestination:
                finalDestination = i  # moves to the next circle to trace back
                path.append(finalDestination)  # keeps track of where we've gone
                # print(path)
                break

    path = list(dict.fromkeys(path))  # remove duplicates

    if pathCounter > 1000000:
        print("Unable to find route to initial circle. Conclusion: Not strongly connected")
        # print(path)
        outFile.write("Unable to find route to initial circle. Conclusion: Not strongly connected")
        exit()

inFile.close()


def DataVomit():  # Formatted data check on all Circles for troubleshooting and verification
    print(' \n Data Vomit: \n ')
    for c in range(1, CircleCount + 1):
        print ("################", CircleSet[c].testID)
        print ("Route List: \n ", CircleSet[c].RouteList)
        print ("Odometer: \n ", CircleSet[c].Odometer)
        print ("Visited:")
        print (CircleSet[c].visited)
        print ("Times Visited: ", CircleSet[c].TimesVisited)
        print ("      ")


# Loop checks all visited booleans, a false indicates that not all nodes have been visited.
# Since checked sequentially, Only the last node will have say on when to end the program.
def Visited():
    for j in range(1, CircleCount + 1):

        if CircleSet[j].visited == False:
            return False

        elif ((CircleSet[j].visited == True) and (j == (CircleCount))):
            return True


# Checks average visit count
def TotalChecksCounter():
    Total = 0
    for c in range(1, CircleCount + 1):
        Total += CircleSet[c].TimesVisited
    return Total


    #  ############  Game starts here   ##############

# Metric variables for game rounds, not to be confused with individual round variables
roundsSum = int(0)
maxChecks = int(0)
maxCheckRoundNumber = int(0)
minChecks = int(0)
minCheckRoundNumber = int(0)
circleCheckSum = int(0)
mostCheckedCircle = int(0)
mostCheckedCircleNumber = int(0)
leastCheckedCircle = int(1000005)  # No number should go this high
leastCheckedCircleNumber = int(-1)

for g in range(1, gameRounds + 1):

    print("##########################################  Round:" + str(g))  # Hash marks for easy readability
    outFile.write("##########################################  Round:" + str(g))
    Marker = int(1)  # Game piece
    Round = 1  # Iteration counter, will always be higer than the total number of visits since the initial circle is not visited in the first round.
    CircleSet[1].TimesVisited = -1  # This fixes an inaccuracy in the visit counter

    # Program runs on a while loop, ending when all circles have been visited - This is checked with the Visited() function.
    loopLock = bool(False)
    while (loopLock == False):

        # Randomly obtain next circle to visit from the current circle's route list
        NewMarker = random.choice(CircleSet[Marker].RouteList)

        CircleSet[Marker].Odometer[NewMarker] += 1  # Increment odometer for route
        Marker = NewMarker  # Update the marker for the next round.

        # Update the next circle to be used. Doing this now prevents the first circle from a false positve. Don't move.
        CircleSet[Marker].visited = True
        CircleSet[Marker].TimesVisited += 1  # Increment visit count
        Round = Round + 1  # Increment the round counter before visit check for accurate round counting

        LoopLock = Visited()  # Check to see if end game conditions have been met.
        if (LoopLock == True):
            break
        if (Round > 1000000):  # Sanity stop
            print("Warning: Million Mark Emergency Stop Activated")
            outFile.write("Warning: Million Mark Emergency Stop Activated")

            break

    # Data Output #########################################################
    print("Circles Used: ", CircleCount)
    print("Arrows Used: ", Round)
    TotalChecks = TotalChecksCounter()
    AvgChecks = TotalChecks / CircleCount
    print("Total number of Checks: ", TotalChecks)
    print("Average of Checks: ", AvgChecks)

    outFile.write("\n")
    outFile.write("Circles Used: " + str(CircleCount))
    outFile.write("\n")
    outFile.write("Arrows Used: " + str(Round))
    outFile.write("\n")
    outFile.write("Total number of Checks: " + str(TotalChecks))
    outFile.write("\n")
    outFile.write("Average of Checks: " + str(AvgChecks))
    outFile.write("\n")

    # Checks TimesVisited varible in Circles class to determine which circle has been visited the most.
    MostVisits = int(0)
    CurrentVisits = int(0)
    CircleMostVisited = int(0)
    for c in range(1, CircleCount + 1):
        CurrentVisits = CircleSet[c].TimesVisited
        if CurrentVisits > MostVisits:
            MostVisits = CurrentVisits
            CircleMostVisited = c

    # Checks TimesVisited varible in Circles class to determine which circle has been visited the least.
    LeastVisits = int(0)
    CurrentVisits2 = int(1000000)
    CircleLeastVisited = int(0)
    for d in range(1, CircleCount + 1):
        CurrentVisits2 = CircleSet[d].TimesVisited
        if (CurrentVisits2 > LeastVisits):
            LeastVisits = CurrentVisits
            CircleLeastVisited = d

    print("Most checked was: " + str(CircleMostVisited) + " with: " + str(MostVisits) + " checks.")
    outFile.write("Most checked was: " + str(CircleMostVisited))
    outFile.write(" with a check count of: " + str(MostVisits))
    outFile.write("\n")

    roundsSum += Round  # for average

    if Round > maxCheckRoundNumber:  # for max number of checks
        maxChecks = Round
        maxCheckRoundNumber = g

    if minChecks < LeastVisits:  # for min number of checks
        minChecks = LeastVisits
        minCheckRoundNumber = g

    circleCheckSum += CircleCount  # for average circle visits

    if (MostVisits > mostCheckedCircle):  # Check most visited
        mostCheckedCircle = CurrentVisits2
        mostCheckedCircleNumber = CircleMostVisited

    if (LeastVisits < leastCheckedCircle):  # Check least visited
        leastCheckedCircle = LeastVisits
        leastCheckedCircleNumber = CircleLeastVisited

print("\n########## End of Game Stats ##########")
outFile.write("\n")
outFile.write("########## End of Game Stats ##########")
avgGameChecks = roundsSum / gameRounds
print("Average number of checks per game:  " + str(avgGameChecks))
outFile.write("\n")
outFile.write(("Average number of checks per game:  " + str(avgGameChecks)))

print("The maximum number of total checks in a single game was round: "
      + str(maxCheckRoundNumber) + " with " + str(maxChecks))
outFile.write("\n")
outFile.write("The maximum number of total checks in a single game was round: "
              + str(maxCheckRoundNumber) + " with " + str(maxChecks))

print("The minimum number of total checks in a single game was round: "
      + str(minCheckRoundNumber) + " with " + str(minChecks))
outFile.write("\n")
outFile.write("The minimum number of total checks in a single game was round: "
              + str(minCheckRoundNumber) + " with " + str(minChecks))

avgSingleCircle = circleCheckSum / gameRounds
avgSingleCircle = (str(avgSingleCircle))
print("The average number of checks on a single circle over all the games: " + avgSingleCircle)
outFile.write("\n")
outFile.write("The average number of checks on a single circle over all the games: " + avgSingleCircle)

print("The minimum number of single circle checks was circle: ")
print(str(leastCheckedCircleNumber) + " with " + str(leastCheckedCircle))
outFile.write("\n")
outFile.write("The minimum number of single circle checks was circle: ")
outFile.write(str(leastCheckedCircleNumber) + " with " + str(leastCheckedCircle))

print("The maximum number of single circle checks was circle: ")
print(str(mostCheckedCircleNumber) + " with " + str(mostCheckedCircle))
outFile.write("\n")
outFile.write("The minimum number of single circle checks was circle: ")
outFile.write(str(mostCheckedCircleNumber) + " with " + str(mostCheckedCircle))

outFile.close()  # Close output file

# DataVomit() #Prints data to screen for troubleshooting and verification

exit()
