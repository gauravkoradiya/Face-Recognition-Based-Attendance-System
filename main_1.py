import tkinter as tk
import time


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)

app=App()



from tkinter import *

import time
tk=Tk()
def clock():
    t=time.asctime(time.localtime(time.time()))
    if t!='':
        label1.config(text=t,font='times 25')
    tk.after(100,clock)
label1=Label(tk,justify='center')
label1.pack()
clock()
tk.mainloop()


from tkinter import *
import time

root = Tk()
root.title("Sourcecodester")
width = 600
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2)- (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="light blue")


#===========================================METHODS=======================================
def tick():
    setTime = time.strftime('%I: %M %S %p')
    clock.config(text=setTime )
    clock.after(200, tick)

#===========================================FRAMES========================================
Top = Frame(root, width=600, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=600)
Mid.pack(side=TOP, expand=1)


#===========================================LABEL WIDGET==================================

clock = Label(Mid, font=('times', 50 , 'bold'), fg="green", bg="light blue")
clock.pack()



#===========================================INITIALIZATION================================
if __name__ == '__main__':
    tick()
    root.mainloop()


