import pygame
from pygame.locals import *
import tkinter as tk
import sys, argparse, os
from random import *

def main():
    root = tk.Tk()
    parser = argparse.ArgumentParser()
    clock = pygame.time.Clock()

    #variables
    image = None #image to edit
    brushColor = (0,0,0)
    brushRadius = 5

    #system arguments
    parser.add_argument('--image', help='Image to view or edit')
    parser.add_argument('--w', help='Image Width')
    parser.add_argument('--h', help='Image Height')
    args = parser.parse_args()

    #tkinter stuff
    text = tk.Button(root, text='garbage')
    text.pack()

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
    screen = pygame.display.set_mode((screenSize))

    if image == None:
        screen.fill((255,255,255))
    else:
        screen.blit(image,(0,0))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen,brushColor,pos,brushRadius)

        print(pygame.mouse.get_pos())

        #rx, ry = randint(0,screenSize[0]), randint(0,screenSize[1])
        #pygame.draw.circle(screen,(255,0,0),(rx,ry),30)

        root.update()
        pygame.display.update()
    
main()
