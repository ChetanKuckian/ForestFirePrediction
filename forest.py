# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 20:46:27 2018

@author: F34R
"""

import pandas
import matplotlib.pyplot as plt
import math


fire = pandas.read_csv("forestfires.csv")
print(fire.columns)
print(fire.shape)

columns = fire.columns.tolist()
columns = [c for c in columns if c not in ["X", "Y", "month", "day", "area", "ISI", "rain", "FFMC", "DMC"]]

print(columns)
fires = fire[fire.area > 0]
fires = fires.loc[:, ['DC', 'temp', 'RH', 'wind']]
print(fires)


initialPopulation = []
currentPopulation = []

def calcFddi(DF, RH, T, U):
    fddi = 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U)
    return fddi

def addToPopulation(memberToAdd):
    currentPopulation.append(memberToAdd)
        
def selectPopulation():
    for item in initialPopulation:
        item.append(calcFddi(item[0],item[1],item[2],item[3]))
    initialPopulation = sorted(initialPopulation,key=lambda x: (x[4]))
    n = len(initialPopulation)
    
    for i in range(0,n/2):
        currentPopulation.append(initialPopulation[i])
     