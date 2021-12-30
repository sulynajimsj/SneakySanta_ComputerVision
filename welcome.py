# Import module
import os
from tkinter import *
def move():
    root.quit()
    os.system("python sneakysanta.py")



# Create object
root = Tk()

# Adjust size
root.geometry("800x800")

# Add image file
bg = PhotoImage(file="christmas.png")

# Create Canvas
canvas1 = Canvas(root, width=400,
                 height=400)

canvas1.pack(fill="both", expand=True)

# Display image
canvas1.create_image(0, 0, image=bg,
                     anchor="nw")

# Add Text
canvas1.create_text(410,288, fill="lightgreen",  font="Times 50 italic bold", text="SneakySanta")
canvas1.create_text(410, 450, fill="white",  font="Times 11 bold", text="You are santa: deliver gift to christmas tree without getting caught\n\n"
                                                                   "Rules: \n"
                                                                   "1. GreenLight: GO (to move you must run with knees high)\n"
                                                                   "2. Redlight: STOP (do not move at red light)\n"
                                                                   "3. As you move knees, the white dot moves\n"
                                                                   "4. When white dot passes endpoint you Win\n"
                                                                   "5. Make sure you are in frame. Press Start to begin MERRY CHRISTMAS :)\n")
# Create Buttons
button1 = Button(root, text="Start",command=move, anchor = W)

# Display Buttons
button1_canvas = canvas1.create_window(400, 550,
                                       anchor="nw",
                                       window=button1)

# Execute tkinter
root.mainloop()


