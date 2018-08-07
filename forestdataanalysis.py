# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 19:28:55 2018

@author: F34R
"""

import pandas
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import os


def calcFddi(DF,T,RH, U):
    fddi = 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U)
    return int(fddi)

currentPopulation = []


fire = pandas.read_csv("forestfires.csv")
print(fire.columns)
print(fire.shape)

fire = fire[fire.area > 0]
column = fire.columns.tolist()
column = [c for c in column if c not in ["X", "Y", "month", "day", "DC","FFMC","ISI","rain","area"]]
print(column)
fire = fire[column]

fire.reset_index(drop = True,inplace = True)
NewMax = 10
NewMin = 1
OldMin = fire['DMC'].min()
OldMax = fire['DMC'].max()



fire.loc[:,'fddi'] = pandas.Series(0, index=fire.index)

for i in range(len(fire.index)):
    fire.at[i,'DMC'] = int((((fire.at[i,'DMC'] - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
    #fire.at[i,'area'] = math.log(fire.at[i,'area'])
    fire.at[i,'fddi'] = calcFddi(fire.at[i,'DMC'],fire.at[i,'temp'],fire.at[i,'RH'],fire.at[i,'wind'])
fires = fire.sort_values('fddi', ascending = False) 
fires.reset_index(drop = True,inplace = True)


for i in range(0,50):
    currentPopulation.append(list(map(int,fire.loc[i].values)))
print(len(currentPopulation))  

AllMinMax = [[1,10],[fire['temp'].min(),fire['temp'].max()],[fire['RH'].min(),fire['RH'].max()],[fire['wind'].min(),fire['wind'].max()]]

def mutateChild(child):
    index = random.sample(range(0,3),2)
    child[index[0]] = random.randint(int(AllMinMax[index[0]][0]),int(AllMinMax[index[0]][1]))    
    return child

def makeChildren():
    parentsIndex = random.sample(range(0,49),2)
    parents = [currentPopulation[parentsIndex[0]],currentPopulation[parentsIndex[1]]]
    temp = parents[0]
    parents[0][1:] = parents[1][1:]
    parents[1][1:] = temp[1:]
    
    x = random.randint(1,101)
    if(x in [6, 23, 47, 62, 81, 94]):
        y = random.randint(0,1)
        parents[y] = mutateChild(parents[y])
        
    parents[0][-1] = calcFddi(parents[0][0],parents[0][1],parents[0][2],parents[0][3])
    parents[1][-1] = calcFddi(parents[1][0],parents[1][1],parents[1][2],parents[1][3])    
    return parents
    
while(len(currentPopulation) != 100):
    child = makeChildren()
    currentPopulation.append(child[0])
    currentPopulation.append(child[1])

for i in range(0,101):
     #os.system('clear')
     
     currentPopulation = sorted(currentPopulation,key=lambda x: (x[4]),reverse = True)
     currentPopulation = currentPopulation[0:50][:]
    
     while(len(currentPopulation) != 100):
         
         child = makeChildren()
         currentPopulation.append(child[0])
         currentPopulation.append(child[1])

def printpop():
    for i in range(len(currentPopulation)):
        print(currentPopulation[i])
        
printpop()        
#print(currentPopulation)  
#print(fire.corr()["area"])
#plt.scatter(fire['area'],fire['fddi'])
