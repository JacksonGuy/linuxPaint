import pygame
from pygame.locals import *
import tkinter as tk
import sys, argparse, os
import numpy as np
from random import *

def brush1(event):
    global brushColor
    pygame.draw.circle(screen,(brushColor),(event.x,event.y),brushRadius)

def saveFrame(event):
    global editArray
    pxarray = pygame.surfarray.array3d(screen)
    frameArray.append(pxarray)
    if len(frameArray) > 15: #frameArray stores last 15 changes made to image
        frameArray.remove(frameArray[0])
    if len(editArray) > 1:
        editArray = [] #clear edit array on change made

def undoFrame():
    currentPxArray = frameArray[-1] #current frame
    editArray.append(currentPxArray) #save current image incase of redo
    lastPxArray = frameArray[-2] #get second most recent frame

    pygame.surfarray.blit_array(screen, lastPxArray)
    del frameArray[-1]

def redoFrame():
    pygame.surfarray.blit_array(screen, editArray[-1])
    del editArray[-1]

def set_rgb_color():
    global brushColor
    r = app1.r_entry.get()
    g = app1.g_entry.get()
    b = app1.b_entry.get()
    brushColor = (int(r),int(g),int(b))

class toolsApp:
    def __init__(self,master):
        self.master = master

        self.button1 = tk.Button(self.master,text='Brush',command=set_rgb_color).grid(row=0,column=0)

        self.r_text = tk.Label(self.master, text="Red Value")
        self.r_text.grid(row=1,column=0)
        self.r_entry = tk.Entry(self.master)
        self.r_entry.grid(row=1,column=1)
        
        self.g_text = tk.Label(self.master, text="Green Value")
        self.g_text.grid(row=2,column=0)
        self.g_entry = tk.Entry(self.master)
        self.g_entry.grid(row=2,column=1)
        
        self.b_text = tk.Label(self.master, text="Blue Value")
        self.b_text.grid(row=3,column=0)
        self.b_entry = tk.Entry(self.master)
        self.b_entry.grid(row=3,column=1)

#windows
root = tk.Tk()
toolWindow = tk.Toplevel()

parser = argparse.ArgumentParser()
clock = pygame.time.Clock()

#variables
image = None #image to edit
global brushColor
brushColor = (0,0,0)
brushRadius = 5
frameArray = [] #after edit is made to image, pixelArray is stored here
editArray = [] #if an undo is made, discarded pixelArray is stored here

#system arguments
parser.add_argument('--image', help='Image to view or edit')
parser.add_argument('--w', help='Image Width')
parser.add_argument('--h', help='Image Height')
args = parser.parse_args()

#tkinter stuff
#menu
menubar = tk.Menu(root)
root.config(menu=menubar)

filesMenu = tk.Menu(menubar,tearoff=0)
filesMenu.add_command(label="Open")
filesMenu.add_command(label="Save")
editMenu = tk.Menu(menubar,tearoff=0)
editMenu.add_command(label="Undo",command=undoFrame)
editMenu.add_command(label="Redo",command=redoFrame)
menubar.add_cascade(label="File", menu=filesMenu)
menubar.add_cascade(label="Edit", menu=editMenu)

#applications
app1 = toolsApp(toolWindow)

if args.w != None and args.h != None:
    screenSize = (int(args.w),int(args.h))
elif args.image != None:
    image = pygame.image.load(str(args.image))
    screenSize = image.get_rect().size
else:
    screenSize = (800,600)

embed = tk.Frame(root,width=screenSize[0], height=screenSize[1])
embed.pack()
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
root.update()

#pygame
pygame.display.init()
screen = pygame.display.set_mode(screenSize)

#keyboard bindings
embed.bind("<B1-Motion>",brush1)
embed.bind("<ButtonRelease-1>",saveFrame)

if image == None:
    screen.fill((255,255,255))
else:
    screen.blit(image,(0,0))

pxarray = pygame.surfarray.array3d(screen)
frameArray.append(pxarray)

while True:
    #print(pygame.mouse.get_pos())
    #rx, ry = randint(0,screenSize[0]), randint(0,screenSize[1])
    #pygame.draw.circle(screen,(255,0,0),(rx,ry),30)

    pygame.display.update()
    root.update()

