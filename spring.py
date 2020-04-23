#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:22:15 2020

@author: daniel
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygame as pg

class Spring:
    def __init__(self, spring_constant = 1, length = 1):
        self.spring_constant = spring_constant
        self.length = length
    
    def attach(self, A, B):
        self.A = A
        self.B = B
    
    def update(self):
        stretch = np.linalg.norm(self.A.pos - self.B.pos) - self.length
        force = stretch * self.spring_constant
        direction = (self.B.pos - self.A.pos)/np.linalg.norm(self.B.pos-self.A.pos)
        force *= direction
        self.A.acceleration += force / self.A.mass
        self.B.acceleration -= force / self.B.mass
#        return direction * force

class Static_Point:
    def __init__(self, pos = np.array([0,0])):
        self.pos = pos
        self.acceleration = np.array([0,0], dtype = np.float64)
        self.mass = 1000

class Mass:
    def __init__(self, mass = 5, pos = np.array([0,0], dtype = np.float64)):
        self.mass = mass
        self.pos = pos
        self.velocity = np.zeros_like(self.pos)
        self.acceleration = np.zeros_like(self.pos)
        self.current_force = self.mass * self.acceleration
        self.trace = np.zeros_like(self.pos)
    
    def update(self):
        
        self.acceleration += np.array([0,0.5])
#        for force in forces:
#            self.acceleration += force / self.mass
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.trace = np.vstack([self.trace, self.pos])
        self.acceleration *= 0
        
class System:
    def __init__(self):
        self.anchor_point1 = Static_Point(np.array([100,300], dtype = np.float64))
        self.anchor_point2 = Static_Point(np.array([600,300], dtype = np.float64))
        self.anchor_point3 = Static_Point(np.array([100,500], dtype = np.float64))
        self.anchor_point4 = Static_Point(np.array([600,500], dtype = np.float64))
        self.spring1 = Spring(length = 50, spring_constant = 2)
        self.spring2 = Spring(length = 50, spring_constant = 2)
        self.spring3 = Spring(length = 50, spring_constant = 2)
        self.spring4 = Spring(length = 50, spring_constant = 2)
        self.spring5 = Spring(length = 50, spring_constant = 2)
        self.spring6 = Spring(length = 50, spring_constant = 2)
        self.spring7 = Spring(length = 50, spring_constant = 2)
        self.mass1 = Mass(mass = 200, pos = np.array([200,300],dtype = np.float64))
        self.mass2 = Mass(mass = 200, pos = np.array([300,300],dtype = np.float64))
        self.mass3 = Mass(mass = 200, pos = np.array([400,300],dtype = np.float64))
        self.mass4 = Mass(mass = 200, pos = np.array([500,300],dtype = np.float64))
        self.spring1.attach(self.anchor_point1, self.mass1)
        self.spring2.attach(self.mass1, self.mass2)
        self.spring3.attach(self.mass2, self.mass3)
        self.spring4.attach(self.mass3, self.mass4)
        self.spring5.attach(self.mass4, self.anchor_point2)
        
        self.spring6.attach(self.mass1, self.anchor_point3)
        self.spring7.attach(self.mass4, self.anchor_point4)
        
        self.springs = [self.spring1, self.spring2, self.spring3, self.spring4, self.spring5, self.spring6, self.spring7]
        self.masses = [self.mass1, self.mass2, self.mass3, self.mass4]
        self.anchor_points = [self.anchor_point1, self.anchor_point2, self.anchor_point3, self.anchor_point4]
        self.alive = False
    
    def run(self):
        self.alive = True
        t = 0
        pg.init()
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode([800,1000])
        
        while self.alive:
            self.display.fill([0,0,0])
            for spring in self.springs:
                spring.update()
            for mass in self.masses:
                mass.update()
            for spring in self.springs:
                pg.draw.line(self.display, (255,255,255), spring.A.pos.astype(int),spring.B.pos.astype(int), 1)
            for mass in self.masses:
                pg.draw.circle(self.display, (255,255,255), mass.pos.astype(int), 10)
            for anchor in self.anchor_points:
                pg.draw.circle(self.display, (255,0,0), anchor.pos.astype(int), 10, 1)
                
            for event in pg.event.get():                    
                if event.type == pg.QUIT:
                    self.alive = False                
            pg.display.update()
            self.clock.tick(60)
            t+=1
            
        fig, axes = plt.subplots(1,3, figsize = (15,5), constrained_layout = True)
        axes = axes.ravel()
        for ax in axes:
            ax.invert_yaxis()
        for mass in self.masses:
            trace = mass.trace[1:]
            axes[0].plot(trace[:,0])
            axes[1].plot(trace[:,1])
            axes[2].plot(trace[:,0], trace[:,1], alpha = 0.5)
            
        axes[0].set_title("Horizontal Movement")     
        axes[1].set_title("Vertical Movement")     
        axes[2].set_title("Mass Trajectory")
        plt.show()
        pg.quit()
            
        
if __name__=="__main__":
    s = System()
    s.run()
        
        
        
        
        