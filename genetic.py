# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 20:00:50 2018

@author: F34R
"""


import pandas
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import os



class genetic:
    
    #For Calculating FDDI
    def calcFddi(DF,T,RH,U):
        fddi = 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U)
        return int(fddi)
    
    #Trying to plot after each generation
    def printPop(population,generation):
        plt.scatter(generation, population)
    
    #Performs mutation    
    def mutateChild(child):
        index = random.sample(range(0,3),2)
        child[index[0]] = random.rand(AllMinMax[index[0]][0],AllMinMax[index[0]][1])
        child[index[1]] = random.rand(AllMinMax[index[1]][0],AllMinMax[index[1]][1])    
        return child    
    
    #Creates children
    def makeChildren(parents):
        temp = parents[0]
        parents[0][1:] = parents[1][1:]
        parents[1][1:] = temp[1:]

        x = random.randint(1,101)
        if(x == 6):
            y = random.randint(0,1)
            parents[y] = mutateChild(parents[y])
        
        parents[0][-1] = calcFddi(parents[0][0],parents[0][1],parents[0][2],parents[0][3])
        parents[1][-1] = calcFddi(parents[1][0],parents[1][1],parents[1][2],parents[1][3])    
        return parents
       
    #Selects Parents for Mating
    def selectParents():
        val = True
        while val:
            parentsIndex = random.sample(range(0,49),2)
            parents = [currentPopulation[parentsIndex[0]],currentPopulation[parentsIndex[1]]]
            if not(parents in matedCouples or parents[0] is parents[1]):
                val = False
        matedCouples.append(parents)
        return parents
    
    #Add From currentPopulation to nextGeneration
    def addToNextGen():
        pop = []
        nextGeneration.clear()
        for person in currentPopulation:
            if person not in pop:
                pop.append(person)
                nextGeneration.append(person)

