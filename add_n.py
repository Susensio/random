from tkinter import *
from random import randint

root = Tk()
root.title("ADD 1")

# tkFont.nametofont('TkDefaultFont').configure(family='Source Code Pro', size=150)

number = StringVar()
number.set("")
text = Label(root, textvariable=number, width=4, anchor=W, padx=50, font=('Source Code Pro', 150))
text.pack()


def setnum():
    mode = 0
    time = 0

    def inner():
        """
        MODES:
        0 => Show number
        1 =>
        """
        nonlocal mode
        nonlocal time

        if mode == 0:
            num = number.get()
            number.set(num + str(randint(0, 9)))
            if len(num) == 3:
                mode = 1

        elif mode == 1:
            number.set("")
            time += 1
            if time == 2:
                time = 0
                mode = 2

        elif mode == 2:
            time += 1
            number.set("*" * time)
            if time == 4:
                mode = 3
                time = 0

        elif mode == 3:
            mode = 0
            number.set("")

        root.after(1000, inner)

    inner()


setnum()
root.mainloop()
