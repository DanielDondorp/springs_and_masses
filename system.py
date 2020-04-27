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
from components import Mass, Spring, Moving_Point, Static_Point


        
class System:
    def __init__(self):
        self.alive = False
        self.components = {}
    
    def add_component(self, name, component):
        self.components[name]=component
    
    def run(self):
        self.alive = True
        t = 0
        pg.init()
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode([800,1000])
        
        while self.alive:
            self.display.fill([0,0,0])
            for component in self.components:
                c = self.components[component]
                c.update()
            
            for component in self.components:
                c = self.components[component]
                c.draw(self.display)
                
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
        self.masses = [self.components[x] for x in self.components if type(self.components[x]) == type(Mass())]
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
        
#    def add_spring(self):
            
        
if __name__=="__main__":
    s = System()
    
    components = {
                "anchor1": Static_Point(pos = np.array([400,100])),
                "mass1": Mass(mass = 100, pos = np.array([500, 100], dtype = np.float64)),
                "mass2": Mass(mass = 150, pos = np.array([600, 100], dtype = np.float64))
                }
    components["spring1"] = Spring(components["anchor1"], components["mass1"], length=50)
    components["spring2"] = Spring(components["mass1"], components["mass2"], length=50)
    
    components["moving1"] = Moving_Point(components["anchor1"].pos.copy())
    components["spring3"] = Spring(components["moving1"], components["mass2"], length = 50)
    
    s.components = components
    
    
    
    
    
    s.run()
        
        
        
        
        