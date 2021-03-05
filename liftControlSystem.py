from tkinter import *
from typing import List
import time
from random import randint

class LiftAlgorithm(Frame):
    """ Main class to run the algorithm.
        Includes Tkinter interface elements.     
    """
    
    def __init__(self, master):
        """ Main method. Launches the configuration options then
            runs the algorithm
        """
        
        super().__init__(master)   
        self.master.title("Lift Algorithm") 
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        
        #create floors entry
        self.floors = Entry(self.canvas)
        self.canvas.create_text((400, 60), text="Floors:", font=("Times", 15))
        self.canvas.create_window(520,60,window=self.floors)
        
        #create people entry
        self.people = Entry(self.canvas)
        self.canvas.create_text((400, 80), text="People:", font=("Times", 15))
        self.canvas.create_window(520,80,window=self.people)
        
        #create capacity entry
        self.capacity = Entry(self.canvas)
        self.canvas.create_text((400, 100), text="Capacity:", font=("Times", 15))
        self.canvas.create_window(520,100,window=self.capacity)
        
        #submit data button  
        self.submitButton = Button(self.canvas, text="Submit", command=self.start_lift)
        self.canvas.create_window(450,150,window=self.submitButton)
        
        self.canvas.pack(fill=BOTH, expand=1)

       
    def start_lift(self) -> None:
        """ Main function that runs the code to the end.
            Starts when submitButton is pressed.
        """
        
        #get the input values
        self.floors_temp = self.floors.get()
        self.people_temp = self.people.get()
        self.capacity_temp = self.capacity.get()
            
        try:
            
            #validate user input
            self.floors_temp = int(self.floors_temp)
            self.people_temp = int(self.people_temp)
            self.capacity_temp = int(self.capacity_temp)
            
        except ValueError:
            print("Not valid.")
            
        else:
            
            #replace the if statement in case a limit for the floors, people and capacity is wanted
            if 1==2: #self.floors_temp > 38 or self.people_temp > 100 or self.capacity_temp > 15:
                print("Out of range.")
            else:
                self.submitButton.destroy()
                
                SLEEP = 0.2 #can be modified for faster walk through
                maxSize = self.floors_temp * 20 + 10
                currentFloor = 0
                peopleList = create_people(self.people_temp, self.floors_temp)
                peopleInLift = []
                capacity = self.capacity_temp
                totalTime = 0 #every lift move counts as 1 time
                totalWaitTime = 0 #every lift move any person waited counts as 1 time
                
                #create the lift with the certain amount of floors
                while currentFloor < self.floors_temp:
                    
                    self.canvas.create_rectangle(10, maxSize - 20 * currentFloor - 20, 30, maxSize - 20 * currentFloor, outline="black", fill="lightgrey")
                    
                    #create people wanting to get in the lift
                    i = 0
                    j = 0
                    while i < len(peopleList):
                        if peopleList[i][0] == currentFloor:
                            self.canvas.create_oval(60 + 25 * j, maxSize - 20 * currentFloor - 20, 40 + 25 * j, maxSize - 20 * currentFloor, outline="black", fill="yellow")
                            self.canvas.create_text(50 + 25 * j, maxSize - 20 * currentFloor - 10, text = str(peopleList[i][1]), tags = "text")
                            j += 1  
                        i += 1
                    currentFloor += 1
                              
                currentFloor = 0
                self.canvas.create_rectangle(10, maxSize - 20 * currentFloor - 20, 30, maxSize - 20 * currentFloor, outline="black", fill="red")
                self.canvas.update()
                time.sleep(SLEEP)
    
                up = True #used to declare the movement of the lift
                maxCapacity = False #used to find out whether the lift is full
                
                """               <<< MAIN LIFT ALGORITHM >>>                """
                while True:
                     
                    #people get removed from the lift FIRST if they reached the floor they wanted to go to
                    i = 0
                    while i < len(peopleInLift):
                        if peopleInLift[i][1] == currentFloor:
                            totalWaitTime += peopleInLift[i][2]
                            peopleInLift.remove(peopleInLift[i])
                            i -= 1
                        i += 1
                    
                    #loop ends when there is no more people waiting for the lift or in the lift
                    if peopleList == [] and peopleInLift == []:
                        break
                    
                    #update and sort the peopleList based on the current floor
                    update_distance(peopleList, up, self.floors_temp)
                    quickSort(peopleList, 0, len(peopleList) - 1)
                    
                    #people get in the lift AFTER if there is space in the lift
                    i = 0
                    while i < len(peopleList) and len(peopleInLift) != capacity:
                        if peopleList[i][0] == currentFloor:
                            self.canvas.create_text(50 + 25 * peopleList[i][3], maxSize - 20 * currentFloor - 10, text = "X", tags = "text", font = "bold")
                            peopleInLift.append(peopleList[i])
                            peopleList.remove(peopleList[i])
                            i -= 1
                        i += 1
                    
                    #check if the lift is full
                    if len(peopleInLift) == capacity:
                        maxCapacity = True
                    else:
                        maxCapacity = False
                        
                    #change direction if necessary
                    up = change_direction(peopleList, peopleInLift, currentFloor, up, maxCapacity)
                    
                    #next floor  
                    self.canvas.create_rectangle(10, maxSize - 20 * currentFloor - 20, 30, maxSize - 20 * currentFloor, outline="black", fill="lightgrey")  
                    if up == True:
                        currentFloor += 1
                    else:
                        currentFloor -= 1
                    
                    #updates after 1 successful lift move
                    self.canvas.create_rectangle(10, maxSize - 20 * currentFloor - 20, 30, maxSize - 20 * currentFloor, outline="black", fill="red")  
                    self.canvas.create_text(20, maxSize - 20 * currentFloor - 10, text = str(len(peopleInLift)), tags = "text")  
                    self.canvas.update()
                    update_people(peopleList)
                    totalTime += 1
                    time.sleep(SLEEP)
                    
                #display end data       
                self.canvas.create_text(450, 200, text = ("Time taken: " + str(totalTime)), tags = "text")
                self.canvas.create_text(450, 220, text = ("Total wait time: " + str(totalWaitTime)), tags = "text")
                self.canvas.create_text((450, 250), text="Restart the program to run again.", font=("Times", 15))
                
        return

def create_people(peopleCount: int, maxFloors: int) -> List:
    """ Create 2D list of people in form:
    
            [starting floor, end floor, time waited, queue position, distance]
            
        Arguments are the amount of people in the building and how many floors the building has.
        Returns 2D list of peopleCount elements.
    """
    
    i = 0
    peopleList = []
    
    while i < peopleCount:
        
        randomFloor = 0
        randomGoTo = 0
        queuePosition = 0
        
        #make sure the starting floor is not the same as go to floor
        while randomFloor == randomGoTo:
            randomFloor = randint(0, maxFloors - 1)
            randomGoTo = randint(0, maxFloors - 1)
        
        #queue position is used for graphical purposes
        j = 0
        while j < len(peopleList):
            if randomFloor == peopleList[j][0]:
                queuePosition += 1
            j += 1
            
        person = [randomFloor, randomGoTo, 0, queuePosition, 0]
        peopleList.append(person)
        
        i += 1
    
    return peopleList

def change_direction(peopleList: List, peopleInLift: List, currentFloor: int, direction: bool, maxCapacity) -> bool:
    """ Algorithm to answer the question: SHOULD THE LIFT DIRECTION CHANGE?
        
        As long as there is someone inside or ahead of the elevator who wants 
        to go in the current direction, keep heading in that direction.
        
        Once the elevator has exhausted the requests in its current direction, 
        switch directions if there is a request in the other direction.
        
        Returns the newDirection which can be changed or the same.
        
        Note: On the ground and top floor the lift always changes direction
              by logic.
    """
    
    newDirection = direction
    change = True #assume direction should change
    
    #if lift is currently heading up
    if direction == True:
        
        #check if there is anyone in the lift that needs to go UP
        i = 0
        while i < len(peopleInLift):
            if peopleInLift[i][1] - currentFloor > 0:
                change = False
                break
            i += 1
        
        #check if there is anyone waiting ABOVE   
        if maxCapacity == False:
            i = 0
            while i < len(peopleList):
                if change == False:
                    break
                if peopleList[i][0] - currentFloor > 0:
                    change = False
                i += 1
        
        if change == True:
            newDirection = False
    
    #if lift is currently heading down  
    else:
        
        #check if there is anyone in the lift that needs to go DOWN
        i = 0
        while i < len(peopleInLift):
            if currentFloor - peopleInLift[i][1] > 0:
                change = False
                break
            i += 1
        
        #check if there is anyone waiting BELOW    
        if maxCapacity == False:
            i = 0
            while i < len(peopleList):
                if change == False:
                    break
                if currentFloor - peopleList[i][0] > 0:
                    change = False
                i += 1
        
        if change == True:
            newDirection = True

    return newDirection

def update_distance(peopleList: List, direction: bool, floors: int) -> None:
    """ For each person, calculate the distance it would take for them to 
        reach their destination if they got in the lift on this floor.
        Changes [4] for every sublist person.
        
        No returns.
    """
    
    i = 0
    while i < len(peopleList):
        
        #there are 4 scenarios each person can be in based on where they want to go and the direction the lift is moving.
        if peopleList[i][0] < peopleList[i][1] and direction == True:
            peopleList[i][4] = peopleList[i][1] - peopleList[i][0]
        elif peopleList[i][0] < peopleList[i][1] and direction == False:
            peopleList[i][4] = 2 * peopleList[i][0] + (peopleList[i][1] - peopleList[i][0]) 
        elif peopleList[i][0] > peopleList[i][1] and direction == False:
            peopleList[i][4] = peopleList[i][0] - peopleList[i][1]
        else:
            peopleList[i][4] = 2 * (floors - peopleList[i][1]) + (peopleList[i][1] - peopleList[i][0]) 
        
        i += 1
        
    return
        
def partition(peopleList: List, low: int, high: int) -> int: 
    """ Used in conjunction with quickSort() to perform the sorting algorithm.
    
        Returns the current index + 1.
    """
    
    i = low - 1 #index of smaller element
    pivot = peopleList[high][4]
  
    for j in range(low , high):
  
        #if current element is smaller than or equal to pivot 
        if   peopleList[j][4] <= pivot: 
            # increment index of smaller element 
            i += 1
            peopleList[i], peopleList[j] = peopleList[j], peopleList[i] 
  
    peopleList[i + 1], peopleList[high] = peopleList[high], peopleList[i + 1] 
    
    return (i + 1) 

def quickSort(peopleList: List, low: int, high: int) -> None: 
    """ Quick sort algorithm to order the list of people by distances.
    
        No returns.
    """
    
    if low < high: 
        #pi is partitioning index, peopleList[p] is now  at right place 
        pi = partition(peopleList,low,high) 
  
        #separately sort elements before 
        #partition and after partition 
        quickSort(peopleList, low, pi-1) 
        quickSort(peopleList, pi+1, high)
        
    return

def update_people(peopleList: List) -> None:
    """ Increase the wait time for every person by 1.
        
        No returns
    """
    
    i = 0
    while i < len(peopleList):
        peopleList[i][2] += 1
        i += 1
        
    return

class MainFrame():
    """ Class to run the interface object creating adequate window size.
    """
    
    def __init__(self):
        root = Tk()
        root.title('Lift')
        root.geometry("700x780")
        LiftAlgorithm(root)
        root.mainloop()

#run code
if __name__ == '__main__':
    MainFrame()
    