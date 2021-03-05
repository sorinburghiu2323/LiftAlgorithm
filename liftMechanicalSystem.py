from tkinter import *
from typing import List
import time
from random import randint

class LiftAlgorithm(Frame):
    """ Main class to run the algorithm.
        Includes tkinter interface elements.     
    """
    
    def __init__(self, master):
        """ Main method. Launches the configuration options then
            runs the algorithm
        """
        
        super().__init__(master)   
        self.master.title("Lift Algorithm Base Case") 
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

            #use the if statement if limit for the amount of floors, people or capacity is needed
            if 1 == 2:#self.floors_temp > 38 or self.people_temp > 100 or self.capacity_temp > 15:
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

                """<<<             MECHANICAL LIFT ALGORITHM             >>>"""
                while True:
                     
                    #people get removed from the lift FIRST if they reached the floor they wanted to go to
                    i = 0
                    while i < len(peopleInLift):
                        if peopleInLift[i][1] == currentFloor:
                            totalWaitTime += peopleInLift[i][2]
                            peopleInLift.remove(peopleInLift[i])
                            i -= 1
                        i += 1

                    if peopleList == [] and peopleInLift == []:
                        break

                    #people get in the lift AFTER if there is space in the lift
                    i = 0
                    while i < len(peopleList) and len(peopleInLift) != capacity:
                        if peopleList[i][0] == currentFloor:
                            self.canvas.create_text(50 + 25 * peopleList[i][3], maxSize - 20 * currentFloor - 10, text = "X", tags = "text", font = "bold")
                            peopleInLift.append(peopleList[i])
                            peopleList.remove(peopleList[i])
                            i -= 1
                        i += 1
                               
                    self.canvas.create_rectangle(10, maxSize - 20 * currentFloor - 20, 30, maxSize - 20 * currentFloor, outline="black", fill="lightgrey")
                    
                    #check direction of the lift and change it if necessary
                    if currentFloor == self.floors_temp - 1:
                        up = False
                    if currentFloor == 0:
                        up = True
                        
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
                self.canvas.create_text((450, 250), text="Restart the app to run again.", font=("Times", 15))
                
        return

def create_people(peopleCount: int, maxFloors: int) -> List:
    """ Create 2D list of people in form:
    
            [starting floor, end floor, time waited, queue position]
            
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
        
        #queue position is used so people get in the lift in the order they arrive
        j = 0
        while j < len(peopleList):
            if randomFloor == peopleList[j][0]:
                queuePosition += 1
            j += 1
            
        person = [randomFloor, randomGoTo, 0, queuePosition]
        peopleList.append(person)
        
        i += 1
    
    return peopleList

def update_people(peopleList: List) -> None:
    """ Increase the wait time for every person by 1.
    """
    
    i = 0
    while i < len(peopleList):
        peopleList[i][2] += 1
        i += 1

class MainFrame():
    """ Class to run the tkinter object creating adequate window size.
    """
    
    def __init__(self):
        root = Tk()
        root.title('Lift')
        root.geometry("700x780")
        firstPage = LiftAlgorithm(root)
        root.mainloop()

#run code
if __name__ == '__main__':
    MainFrame()
