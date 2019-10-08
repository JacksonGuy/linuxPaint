import pygame
from pygame.locals import *
import tkinter as tk
import sys, argparse, os
from functools import partial

def brush1(event):
    global brushColor
    pygame.draw.circle(drawLayer,(brushColor),(event.x,event.y),brushRadius)

def eraserTool(event):
    global image
    if image == None:
        pygame.draw.circle(drawLayer,pygame.Color(255,255,255),(event.x,event.y),brushRadius)
    else:
        drawLayer.blit(image,(event.x,event.y),pygame.Rect(event.x,event.y,brushRadius,brushRadius))

def saveFrame(event):
    global editArray
    pxarray = pygame.surfarray.array3d(drawLayer)
    frameArray.append(pxarray)
    if len(frameArray) > 15: #frameArray stores last 15 changes made to image
        frameArray.remove(frameArray[0])
    if len(editArray) > 0:
        editArray = [] #clear edit array on change made

def undoFrame(event=None):
    currentPxArray = frameArray[-1] #current frame
    editArray.append(currentPxArray) #save current image incase of redo
    lastPxArray = frameArray[-2] #get second most recent frame

    pygame.surfarray.blit_array(drawLayer, lastPxArray)
    try:
        frameArray.pop()
    except ValueError:
        print('Error removing frame from array')

def redoFrame(event=None):
    pygame.surfarray.blit_array(drawLayer, editArray[-1])
    frameArray.append(editArray[-1])
    del editArray[-1]

def save_image(event=None):
    pygame.image.save(screen, args.n)

def set_rgb_color():
    global brushColor
    r = toolApp.r_entry.get()
    g = toolApp.g_entry.get()
    b = toolApp.b_entry.get()
    try:
        brushColor = (int(r),int(g),int(b))
    except ValueError:
        pass
    
    #change tool to brush
    embed.bind("<B1-Motion>",brush1)

def set_color_button(rgb):
    global brushColor
    brushColor = rgb

def set_brush_size():
    global brushRadius
    try:
        brushRadius = int(toolApp.brushSize_entry.get())
    except ValueError:
        pass

class toolsAppInstance:
    def __init__(self,master):
        self.master = master

        self.button1 = tk.Button(self.master,text='Brush',command=set_rgb_color).grid(row=0,column=0)
        self.button2 = tk.Button(self.master,text="Eraser",command=lambda: embed.bind("<B1-Motion>",eraserTool)).grid(row=0,column=1)
        
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

        self.red_color_button = tk.Button(self.master,command=partial(set_color_button,(255,0,0)),bg="#ff0000").grid(row=1,column=2,sticky="e")
        self.green_color_button = tk.Button(self.master,command=partial(set_color_button,(0,255,0)),bg='#00ff00').grid(row=2,column=2,sticky="e")
        self.blue_color_button = tk.Button(self.master,command=partial(set_color_button,(0,0,255)),bg='#0000ff').grid(row=3,column=2,sticky="e")
        self.yellow_color_button = tk.Button(self.master,command=partial(set_color_button,(255,255,0)),bg='#ffff00').grid(row=1,column=3,sticky="e")
        self.purple_color_button = tk.Button(self.master,command=partial(set_color_button,(255,0,255)),bg='#ff00ff').grid(row=2, column=3,sticky="e")
        self.orange_color_button = tk.Button(self.master,command=partial(set_color_button,(255,165,0)),bg="#FFA500").grid(row=3,column=3, sticky="e")
        self.black_color_button = tk.Button(self.master,command=partial(set_color_button,(0,0,0)),bg="#000000").grid(row=1,column=4,sticky="e")
        self.white_color_button = tk.Button(self.master,command=partial(set_color_button,(255,255,255)),bg="#FFFFFF").grid(row=2,column=4,sticky="e")
        self.cyan_color_button = tk.Button(self.master,command=partial(set_color_button,(0,255,255)),bg="#00FFFF").grid(row=3,column=4,sticky="e")

        self.brushSize_text = tk.Label(self.master, text="Brush Size")
        self.brushSize_text.grid(row=4,column=0)
        self.brushSize_entry = tk.Entry(self.master)
        self.brushSize_entry.grid(row=4,column=1)
        self.brushSize_button = tk.Button(self.master,text="Set Brush Size",command=set_brush_size).grid(row=5,column=0)

#windows
root = tk.Tk()
toolWindow = tk.Toplevel()
toolWindow.grid_rowconfigure(10,minsize=10)
toolWindow.grid_columnconfigure(10,minsize=10)

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
parser.add_argument('--n', help='Name to save image as')
args = parser.parse_args()

#tkinter stuff
#menu
menubar = tk.Menu(root)
root.config(menu=menubar)

filesMenu = tk.Menu(menubar,tearoff=0)
filesMenu.add_command(label="Save",command=save_image)
editMenu = tk.Menu(menubar,tearoff=0)
editMenu.add_command(label="Undo",command=undoFrame)
editMenu.add_command(label="Redo",command=redoFrame)
menubar.add_cascade(label="File", menu=filesMenu)
menubar.add_cascade(label="Edit", menu=editMenu)

#applications
toolApp = toolsAppInstance(toolWindow)

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
screen = pygame.display.set_mode(screenSize) #background
drawLayer = pygame.Surface(screenSize, pygame.SRCALPHA, 32)
drawLayer = drawLayer.convert_alpha()

#keyboard bindings
embed.bind("<B1-Motion>",brush1)
embed.bind("<ButtonRelease-1>",saveFrame)
embed.bind_all("<Control-z>",undoFrame)
embed.bind_all("<Control-y>",redoFrame)
embed.bind_all("<Control-s>",save_image)

if image == None:
    screen.fill((255,255,255))
else:
    screen.blit(image,(0,0))

#ok so the next few lines look really stupid but without them the undo function doesnt work
#so we keeping these for now
pxarray = pygame.surfarray.array3d(screen)
frameArray.append(pxarray)
screen.fill((0,0,0))
pxarray = pygame.surfarray.array3d(screen)
frameArray.append(pxarray)
undoFrame()

#set rgb entry with current value
toolApp.r_entry.insert(0,str(brushColor[0]))
toolApp.g_entry.insert(0,str(brushColor[1]))
toolApp.b_entry.insert(0,str(brushColor[2]))
toolApp.brushSize_entry.insert(0,str(brushRadius))

#load addons from json
import importlib.util
import json
with open('addonList.json') as addonFile:
    data = json.load(addonFile)

for addon in data:
    spec = importlib.util.spec_from_file_location(addon, data[addon])
    if spec != None:
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        foo.run(toolApp)

while True:
    screen.blit(drawLayer, (0,0))
    pygame.display.update()
    root.update()

