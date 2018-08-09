import pandas
#import numpy as np
import matplotlib.pyplot as plt
import math
import random


class Genetic:

    # Read dataset and create and sort the initial population
    def __init__(self):
        self.currentPopulation = []
        self.nextGeneration = []
        self.matedCouples = []
        fire = pandas.read_csv("forestfires.csv")
        fire = fire[fire.area > 0]
        column = fire.columns.tolist()
        column = [c for c in column if c not in ["X", "Y", "month", "day", "DC","FFMC","ISI","rain","area"]]
        fire = fire[column]
        fire.reset_index(drop=True, inplace=True)
        NewMax = 10
        NewMin = 1
        OldMin = fire['DMC'].min()
        OldMax = fire['DMC'].max()
        fire.loc[:, 'fddi'] = pandas.Series(0, index=fire.index)
        for i in range(len(fire.index)):
            fire.at[i, 'DMC'] = int((((fire.at[i, 'DMC'] - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
            # fire.at[i,'area'] = math.log(fire.at[i,'area'])
            fire.at[i, 'fddi'] = self.calcFddi(fire.at[i, 'DMC'], fire.at[i, 'temp'], fire.at[i,'RH'], fire.at[i,'wind'])
        fires = fire.sort_values('fddi', ascending=False) 
        fires.reset_index(drop=True,inplace=True)
        for i in range(0, 100):
            self.currentPopulation.append(list(fires.loc[i].values))
        self.currentPopulation = sorted(self.currentPopulation, key=lambda x: (x[4]), reverse=True)
        self.AllMinMax = [[1,10],[20,50],[fire['RH'].min(),fire['RH'].max()],[30,120]]

    # For Calculating fitness function FDDI
    def calcFddi(self, DF, T, RH, U):
        fddi = 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U)
        return int(fddi)

    def mutateChild(self, child):
        indexx = random.sample(range(0,3),2)
        child[indexx[0]] = random.randint(int(self.AllMinMax[indexx[0]][0]),int(self.AllMinMax[indexx[0]][1]))
        child[indexx[1]] = random.randint(int(self.AllMinMax[indexx[1]][0]),int(self.AllMinMax[indexx[1]][1]))    
        return child
    
    # create next generation of individuals
    def createNextGeneration(self):
        #add top 50 individuals from currentPopulation to nextGeneration
        for i in range(0,50):
            self.nextGeneration.append(self.currentPopulation[i])
        # reproduce to fill rest of the population
        while  (len(self.nextGeneration) < 100 ):
            children = self.makeChildren(self.selectParents())
            if (children != None):
                self.nextGeneration.append(children[0])
                self.nextGeneration.append(children[1])
        self.nextGeneration = sorted(self.nextGeneration,key=lambda x: (x[4]),reverse = True)

    # reproduce for nextGeneration
    def makeChildren(self, parents):
        # crossover
        temp = parents[0]
        parents[0][1:] = parents[1][1:]
        parents[1][1:] = temp[1:]

        #mutation
        x = random.randint(1,101)
        if(x == 6):
            y = random.randint(0,1)
            parents[y] = self.mutateChild(parents[y])
        
        parents[0][-1] = self.calcFddi(parents[0][0],parents[0][1],parents[0][2],parents[0][3])
        parents[1][-1] = self.calcFddi(parents[1][0],parents[1][1],parents[1][2],parents[1][3])    
        return parents

    #Selects Parents for Mating
    def selectParents(self):
        val = True
        while val:
            parentsIndex = random.sample(range(0,49),2)
            parents = [self.currentPopulation[parentsIndex[0]],self.currentPopulation[parentsIndex[1]]]
            if not(parents in self.matedCouples or parents[0] is parents[1]):
                val = False
        self.matedCouples.append(parents)
        return parents

    #replace currentPopulation with nextGeneration
    def addToNextGen(self):
        self.currentPopulation = self.nextGeneration[1:100]
        self.nextGeneration.clear()
        self.matedCouples.clear()

    #Trying to plot after each generation
    def printPop(self, population, generation):
        plt.scatter(generation, population)

