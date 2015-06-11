import Tkinter as tk
import tkMessageBox
import sys
import pygame
import pygame.mixer
from PIL import Image, ImageTk


pygame.init() 
root = tk.Tk()
root.title('Ball in Maze')
root.resizable(0,0)

sound = pygame.mixer.Sound("models/menuscreen.ogg")
sound.play(10)


imageFile = "models/menuscreen.gif"
image1 = ImageTk.PhotoImage(Image.open(imageFile))


w = image1.width()
h = image1.height()
 

x = 300
y = 500
 

root.geometry("%dx%d+%d+%d" % (w, h, x, y))
 

panel1 = tk.Label(root, image=image1)
panel1.pack(side='top',fill='both', expand='yes')

 
def startMaze():
	#sound.stop()
	import main

def exitMaze():
	sys.exit()

def helpMaze():
	tkMessageBox.showinfo("HELP", "Move Your Mouse To Tilt The Maze")


B1 = tk.Button(panel1,text ="PLAY", command = startMaze)
B1.place(relx=0.5, rely=0.5, anchor='center',height=50, width=150)
B2 = tk.Button(panel1, text='HELP',command = helpMaze)
B2.place(relx=0.5, rely=0.5, anchor='center',y=60,height=50, width=150)
B3 = tk.Button(panel1, text='EXIT',command = exitMaze)
B3.place(relx=0.5, rely=0.5, anchor='center',y=120,height=50, width=150)



 

panel1.image = image1

 

root.mainloop()
