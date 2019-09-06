import pygame
from pygame.locals import *
import tkinter
import sys, argparse

class Window(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title = "Window 1"
        self.pack(fill=tkinter.BOTH, expand=1)

        #quit button
        quitButton = tkinter.Button(self, text="Quit",command=self.window_exit)
        quitButton.place(x=0, y=0)
    
    def window_exit(self):
        sys.exit()

def get_event():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

def main():
    pygame.init()
    parser = argparse.ArgumentParser()
    
    #system arguments
    parser.add_argument('--image', help='Image to view or edit')
    parser.add_argument('--w', help='Image Width')
    parser.add_argument('--h', help='Image Height')
    args = parser.parse_args()

    if args.image == None:
        screenSize = (int(args.w),int(args.h))
    else:
        pass #get image resolution and set screen to that

    screen = pygame.display.set_mode(screenSize)

    #tkinker
    root = tkinter.Tk()
    root.geometry("400x300")
    app = Window(master=root)
    app.mainloop()

    while True:
        get_event()
        screen.fill((0,0,0))
        pygame.display.flip()

main()