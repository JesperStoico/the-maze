from tkinter import *
from tkinter import Button

tk = Tk()

width = IntVar()
height = IntVar()

def assign_label():
    text = 'Width: {}, Height: {}'.format(width.get(), height.get())
    label.config(text=text)

scale_width = Scale(tk, variable=width)
scale_width.pack()
scale_height = Scale(tk, variable=height)
scale_height.pack()

label = Label()
label.pack() 

create_button = Button(master=tk, text='Create a maze', command=assign_label)
create_button.pack()
tk.mainloop()

