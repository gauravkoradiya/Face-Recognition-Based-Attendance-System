from tkinter import Tk, Canvas
from math import sin, cos, radians
from datetime import datetime

class point():
    """
    A little point class for storing xy pairs,
    + and - are overloaded for the class
    """
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return point(x, y)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return point(x, y)
    def __str__(self):
        return '[x:{0}, y:{1}]'.format(self.x,self.y)
    def offsetByVector(self, angle, length):
        """
        Create point from an origin and a vector
        The vector consistes of a length and an angle in radians
        """
        x = int(cos(angle) * length) + self.x
        y = int(sin(angle) * length) + self.y
        return point(x, y)

class clockHands():
    """
    This class controls the clock Hands, which need to positioned in a
    proper circle to work
    """
    root = Tk()
    #The hand id strings(initialized on the first pass through updateClock)
    longHand = ""
    shortHand = ""
    secondHand = ""
    #The corners of the Circle of the clock
    corner1 = point(10,10)
    corner2 = point(210, 210)
    
    #Get a Tk Window in which to draw the clock 
    
    def centerPoint(self):
        #Use the midpoint formula to get the center of of the clock
        #instead of guessing at the middle of the circle
        x = (self.corner1.x + self.corner2.x)/2
        y = (self.corner1.y + self.corner2.y)/2
        return point(x, y)
    
    
    def updateClock(self, canvas):
        #Conditionally initialize a clock hand
        def initHand(hand, color, width):
            if hand == "":
                hand = canvas.create_line(0,0,0,0,\
                    fill = color, width = width, capstyle = "round")
                canvas.pack()
            return hand
        #This updates all the TK control names to be the same as they have been
        shortHand = self.shortHand = initHand(self.shortHand, "grey", 2)
        longHand = self.longHand = initHand(self.longHand, "black", 4)
        secHand = self.secondHand = initHand(self.secondHand, "red", 1)
        time = datetime.now()
        #The extra amount added to the angles accounts for the
        #slight changes that a clock hand has over the course a rotation
        hourAngle = ((time.hour * 30.0) + (30.0 * (time.minute/60.0)))
        minuteAngle = ((time.minute * 6.0) + (6.0 * (time.second/60.0)))
        secondAngle = (time.second * 6)

        def drawHand(Hand, angle, length):
            #Offset by 90.0 degrees so that we get 0 as the top of the clock,
            #not 3 o'clock, like algebra normally does
            angle -= 30.0
            
            rads = radians(angle)
            center = self.centerPoint()
            endPoint = center.offsetByVector(rads, length)
            canvas.coords(Hand, center.x, center.y, endPoint.x, endPoint.y)

        drawHand(longHand, hourAngle, 50)
        drawHand(shortHand, minuteAngle, 80)
        drawHand(secHand, secondAngle, 90)
        #Recall this function after 100 miliseconds
        rotate = lambda: self.updateClock(canvas)
        print (time)
        canvas.after(100, rotate)
        
    def run(self):
        #Professor Cohen, for kicks, would you use a math pun in your
        #feedback on this assignment? :) -yumaikas 
        self.root.mainloop()

    def __init__(self):
        canvas = Canvas(self.root, width=220, height=220)
        
        #Get the corners of the circle
        corner1 = self.corner1
        corner2 = self.corner2
        
        canvas.create_oval(corner1.x, corner1.y, corner2.x, corner2.y,\
                           fill = "white", width = 3)
        center = self.centerPoint()

        def createTickMark(angle, dFromCenter, length, mark):
            angle -= 90.0
            rads = radians(angle)
            p1 = center.offsetByVector(rads, dFromCenter)
            p2 = center.offsetByVector(rads, dFromCenter + length)
            mark(p1, p2)
        #mark is meant to be one of the below lambdas
        sm_Tick = lambda p1, p2: canvas.create_line(p1.x, p1.y, p2.x, p2.y)
        lg_Tick = lambda p1, p2: canvas.create_line(p1.x, p1.y, p2.x, p2.y,\
                                                    fill = 'red', width=3)
        #Create minute tick marks
        for angle in range(0, 360, 6):
            createTickMark(angle, 90, 9, sm_Tick)
        #Create hour tick marks 
        for angle in range(0, 360, 30):
            createTickMark(angle, 80, 19, lg_Tick)
        #Create extra marks every 3 hours
        for angle in range(0, 360, 90):
            createTickMark(angle, 60, 10, sm_Tick)

        canvas.pack()
        self.root.wm_title("Clock")
        #Prepare the code to be run in the main loop   
        self.updateClock(canvas)
        
def main():
    Hand = clockHands()
    Hand.run()
main()