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

class Snake(object):
    
    def __init__(self, gridSize):        
        self.gameOver = False
        self.sleep = 0.5
        self.x, self.y = gridSize, gridSize
        self.position = [4, 4]
        self.tail = [self.position[0], self.position[1] - 3]
        self.berry_position = None
        self.grid = None
        self.queue_movements = ['right'] * 3
        
        if self.position[1] <= self.y // 2:
            self.direction = 'right'
        else:
            self.direction = 'left'
            
    
    def draw(self):
        os.system("CLS")
        #Snake
        if self.grid is None:
            self.grid = np.array([[' ' for i in range(self.x)] for j in range(self.y)])
            for j in range(3):
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
        
        print(self.position, self.berry_position)
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
#------------------ Play
game = Snake(10)
game.play()