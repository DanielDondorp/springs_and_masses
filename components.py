#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:40:59 2020

@author: daniel
"""
import pygame as pg
import numpy as np

class Spring:
    def __init__(self, A, B, spring_constant = 1, length = 1):
        self.spring_constant = spring_constant
        self.length = length
        self.A = A
        self.B = B
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
    def draw(self, display):
        pg.draw.line(display, (255,255,255), self.A.pos.astype(int),self.B.pos.astype(int), 1)

class Static_Point:
    def __init__(self, pos = np.array([0,0])):
        self.pos = pos
        self.acceleration = np.array([0,0], dtype = np.float64)
        self.mass = 1000
    def update(self):
        pass
    def draw(self, display):
        pg.draw.circle(display, (255,0,0), self.pos.astype(int), 10, 1)
        
class Moving_Point(Static_Point):
    def update(self):
        self.pos += np.array([1,0])

class Mass:
    def __init__(self, mass = 5, pos = np.array([0,0], dtype = np.float64)):
        self.mass = mass
        self.pos = pos
        self.velocity = np.zeros_like(self.pos)
        self.acceleration = np.zeros_like(self.pos)
        self.current_force = self.mass * self.acceleration
        self.trace = np.zeros_like(self.pos)   
    def update(self):
        
        self.acceleration += np.array([0,1])
#        for force in forces:
#            self.acceleration += force / self.mass
        self.velocity += self.acceleration
        self.velocity *= 0.999
        self.pos += self.velocity
        self.trace = np.vstack([self.trace, self.pos])
        self.acceleration *= 0
    def draw(self, display):
        pg.draw.circle(display, (255,255,255), self.pos.astype(int), self.mass // 20)
        