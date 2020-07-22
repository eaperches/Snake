# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 22:21:08 2020

@author: eaper
"""


""" Snake """

import keyboard
import time
import random
import numpy as np
import os

from PIL import Image, ImageTk
import tkinter as tk

class Snake(object):
    
    def __init__(self):        
        self.gameOver = False
        self.sleep = 0.5
        self.snake_length = 3
        self.x, self.y = 10, 10
        self.position = [4, 4]
        self.tail = [self.position[0], self.position[1] - self.snake_length]
        self.berry_position = None
        self.grid = None
        self.queue_movements = ['right'] * self.snake_length
        self.direction = 'right'
    
        #TK
        self.c = None
        self.pollingms = 10
        
    def draw(self, printConsole = True):
        os.system("CLS")
        #Snake
        if self.grid is None:
            self.grid = np.array([[' ' for i in range(self.x)] for j in range(self.y)])
            for j in range(self.snake_length):
                body = [self.position[0], self.position[1] - j]
                self.grid[body[0], body[1]] = 'X'
        else:
            self.grid[self.position[0], self.position[1]] = 'X'
            self.grid[self.tail[0], self.tail[1]] = ' '

        #Berry
        if self.berry_position is None or self.position == self.berry_position:
            empty_spaces = []
            for i in range(self.x):
                for j in range(self.y):
                    if self.grid[i][j] != 'X':
                        empty_spaces.append([i,j])
            self.berry_position = random.choice(empty_spaces)
            self.grid[self.berry_position[0], self.berry_position[1]] = 'B'
            
        if printConsole:
            print(self.grid)
        
    def key_input(self):
        time_out = self.sleep
        start = time.time()
        new_direction = self.direction
        pressed = False
        while(time.time() - start < time_out):
            if not pressed:
                if keyboard.is_pressed('up') and self.direction != 'down':
                    new_direction = 'up'
                    pressed = True
                if keyboard.is_pressed('down') and self.direction != 'up':
                    new_direction = 'down'
                    pressed = True
                if keyboard.is_pressed('left') and self.direction != 'right':
                    new_direction = 'left'
                    pressed = True
                if keyboard.is_pressed('right') and self.direction != 'left':
                    new_direction = 'right'
                    pressed = True
                
        self.direction = new_direction
        
        
    def logic(self):
        def move(position,direction):
            new_position = position
            if direction == 'right':
                new_position[1] += 1
            elif direction == 'left':
                new_position[1] -= 1
            elif direction == 'up':
                new_position[0] -= 1
            elif direction == 'down':
                new_position[0] += 1
                
            return new_position
                
        new_position = move(self.position, self.direction)
        self.queue_movements.append(self.direction)
        
        if self.position != self.berry_position:
            new_tail = move(self.tail, self.queue_movements.pop(0))
        else:
            new_tail = self.tail
        
        if 0 <= new_position[0] < self.x and 0 <= new_position[1] < self.y and self.grid[new_position[0], new_position[1]] != 'X':
            self.position = new_position
            self.tail = new_tail
        else:
            self.gameOver = True

    def play(self):
        while(not self.gameOver):
            self.draw()
            self.key_input()
            self.logic()
        print('Game Over! Thanks for playing!')
        
        
    #TK-------------------------------------------
    def TKdraw(self):
        def createGrid(event=None):
            c = self.c
            w = c.winfo_width() # Get current width of canvas
            h = c.winfo_height() # Get current height of canvas
            c.delete('grid_line') # Will only remove the grid_line
        
            # Creates all vertical lines at intevals of 100
            for i in range(0, w, 100):
                c.create_line([(i, 0), (i, h)], tag='grid_line')
        
            # Creates all horizontal lines at intevals of 100
            for i in range(0, h, 100):
                c.create_line([(0, i), (w, i)], tag='grid_line')
                
            self.tiles = {}
            self.apple_tiles = {}
            for i in range(self.x):
                for j in range(self.y):
                    if self.grid[i][j] == 'X':
                        x1, y1 = i*100, j*100
                        x2, y2 = (i+1)*100, (j+1)*100
                        self.tiles[(i, j)] = c.create_rectangle(y1, x1, y2, x2, fill = "green")
                    elif self.grid[i][j] == 'B':
                        x1, y1 = i*100, j*100
                        x2, y2 = (i+1)*100, (j+1)*100
                        self.apple_tiles[(i, j)] = c.create_rectangle(y1, x1, y2, x2, fill = "red")
                
        def updateGrid(event=None):
            #Snake
            #Update head
            i, j = self.position
            x1, y1 = i*100, j*100
            x2, y2 = (i+1)*100, (j+1)*100
            self.tiles[(i, j)] = self.c.create_rectangle(y1, x1, y2, x2, fill = "green")
            #update tail
            i, j = self.tail
            if self.tiles.get((i, j)):
                self.c.delete(self.tiles[(i, j)])
                self.tiles.pop((i,j), None)
            
            #Berry
            if self.position == self.berry_position:
                i, j = self.position
                self.c.delete(self.apple_tiles[(i, j)])
                empty_spaces = []
                for i in range(self.x):
                    for j in range(self.y):
                        if (i,j) not in self.tiles:
                            empty_spaces.append([i,j])
                self.berry_position = random.choice(empty_spaces)
                i, j = self.berry_position
                x1, y1 = i*100, j*100
                x2, y2 = (i+1)*100, (j+1)*100
                self.apple_tiles[(i, j)] = self.c.create_rectangle(y1, x1, y2, x2, fill = "red")
                    
        if not self.c:
            self.c = tk.Canvas(self.root, height=self.y*100, width=self.x*100, bg='white')
            self.c.pack(fill=tk.BOTH, expand=True)
            
            self.c.bind('<Configure>', createGrid)
        else:
            self.c.after(self.pollingms, updateGrid)
            
        self.c.after(self.pollingms, self.TKkey_input)
        
    def TKkey_input(self):
        time_out = self.sleep
        start = time.time()
        new_direction = self.direction
        pressed = False
        while(time.time() - start < time_out):
            if not pressed:
                if keyboard.is_pressed('up') and self.direction != 'down':
                    new_direction = 'up'
                    pressed = True
                if keyboard.is_pressed('down') and self.direction != 'up':
                    new_direction = 'down'
                    pressed = True
                if keyboard.is_pressed('left') and self.direction != 'right':
                    new_direction = 'left'
                    pressed = True
                if keyboard.is_pressed('right') and self.direction != 'left':
                    new_direction = 'right'
                    pressed = True
                
        self.direction = new_direction
        
        self.c.after(self.pollingms, self.TKlogic)
    
    def TKlogic(self):
        def move(position,direction):
            new_position = position
            if direction == 'right':
                new_position[1] += 1
            elif direction == 'left':
                new_position[1] -= 1
            elif direction == 'up':
                new_position[0] -= 1
            elif direction == 'down':
                new_position[0] += 1
                
            return new_position
                
        new_position = move(self.position, self.direction)
        self.queue_movements.append(self.direction)
        
        if self.position != self.berry_position:
            new_tail = move(self.tail, self.queue_movements.pop(0))
        else:
            new_tail = self.tail
        
        if 0 <= new_position[0] < self.x and 0 <= new_position[1] < self.y and tuple(new_position) not in self.tiles:
            self.position = new_position
            self.tail = new_tail
            self.c.after(self.pollingms, self.TKdraw)
        else:
            self.gameOver = True
            
    def TKplay(self):
        self.root = tk.Tk()
        self.draw(False)
        self.TKdraw()
        self.root.mainloop()
        
        

#------------------ Play
game = Snake()
#game.play() #play in console
game.TKplay() #play with tkinter



