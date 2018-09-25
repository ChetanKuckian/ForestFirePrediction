
# -*- coding: utf-8 -*-


import pandas
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import os
import collections
import copy
import append_to_excel as ex

compare = lambda x,y: collections.Counter(x) == collections.Counter(y)

'''Global Variables'''
currentPopulation = []
nextGeneration = []
matedCouples= []

'''This function  builds the next generations population and stores it in currentPopulation'''
def addToNextGen():
    global currentPopulation,nextGeneration
    pop1 = []
    del currentPopulation[:]
    for person in nextGeneration:
        if len(currentPopulation) == 200:
            break
        if person not in pop1:
            pop1.append(person)
            currentPopulation.append(person)
    while (len(currentPopulation) != 200):
       currentPopulation.append(pop1[random.randint(0,len(pop1)-1)])
    sortPopulation()
            
'''Calculate Ffdi Value'''
def calcFfdi(DF,T,RH, U):
    return int( 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U))

def sortPopulation():
    global currentPopulation
    currentPopulation = sorted(currentPopulation,key=lambda x: (x[4]),reverse = True)
    
    
'''Prints Final Population'''
def printpop():
    for i in range(len(currentPopulation)):
        print(currentPopulation[i])

'''This Function is used for mutating the child passed to it. It randomly replaces  one value from (drought factor, temperature, relative humidity, wind) from within range of values from the guven dataset'''
def mutateChild(child):
    index = random.sample(range(0,4),2)
    child[index[0]] = random.randint(int(AllMinMax[index[0]][0]),int(AllMinMax[index[0]][1]))

    return child

'''This Function selects two random parents from top 150 population and mates them, if the selected parents are already mated then it returns None'''
def makeChildren():
    global nextGeneration,currentPopulation,matedCouples
    parentsIndex = random.sample(range(0,200),2)
    parents = [copy.deepcopy(currentPopulation[parentsIndex[0]]),copy.deepcopy(currentPopulation[parentsIndex[1]])]
    if (parents in matedCouples) or (compare(parents[0],parents[1])):
        return None
    matedCouples.append(copy.deepcopy(parents))  
    i = random.randint(1,3)
    parents[0][i:], parents[1][i:] = parents[1][i:],parents[0][i:]
    x = random.randint(1,101)
    if(x in [6,27,73]):
        y = random.randint(0,1)
        parents[copy.deepcopy(y)] = copy.deepcopy(mutateChild(parents[y]))
        
    parents[0][4] = copy.deepcopy(calcFfdi(parents[0][0],parents[0][1],parents[0][2],parents[0][3]))
    parents[1][4] = copy.deepcopy(calcFfdi(parents[1][0],parents[1][1],parents[1][2],parents[1][3]))
    return parents
        
'''This function is used to create 300 children for nextgeneration which will be sorted and top 200 unique will be selected'''
def createChildren():
    global nextGeneration,currentPopulation
    for i in range(0,50):
        children = None
        while children is None:
            children = makeChildren()   
        nextGeneration.append(copy.deepcopy(children[0]))
        nextGeneration.append(copy.deepcopy(children[1]))

'''This Function is used to stimulate generations'''            
def runGeneration():
    global nextGeneration,currentPopulation,matedCouples
    del nextGeneration[:]
    del matedCouples[:]
    for i in range(0,10):
        nextGeneration.append(copy.deepcopy(currentPopulation[i]))
    createChildren()

    nextGeneration = sorted(nextGeneration,key=lambda x: (x[4]),reverse = True)
    addToNextGen()

def startGenetic(numberOfGeneration,toExcelLength):
    global currentPopulation
    if not(os.path.isfile(r'AllPopulation.xlsx')):
        ex.createSheet("AllPopulation.xlsx")
    
    if not(os.path.isfile(r'BestIndividuals.xlsx')):
        ex.createBestIndividualExcel("BestIndividuals.xlsx",['Generation','FFDI'])

    ch = 1    

    for i in range(numberOfGeneration):
        if i == ch*100 -1:
            print(i+1," Generations completed!!!!")
            ch +=1
        runGeneration()
        ex.bestIndividualToExcel("BestIndividuals.xlsx",[i+1,currentPopulation[0][-1]],['Generation','FFDI'])
        if i==0:
            continue
        elif i % toExcelLength == 0:
            ex.appendToExcel("AllPopulation.xlsx",currentPopulation)
        elif i == numberOfGeneration -1:
            ex.appendToExcel("AllPopulation.xlsx",currentPopulation)



'''importing data using pandas'''
fire = pandas.read_csv("forestfires.csv")
print(fire.columns)
print(fire.shape)

fire.loc[:,'Ffdi'] = pandas.Series(0, index=fire.index)

'''selecting only those values from dataset where area is greater than 0'''
fire = fire[fire.area > 0]
column = fire.columns.tolist()
'''Removing all unwanted columns'''
column = [c for c in column if c not in ["X", "Y", "month", "day", "DC","FFMC","ISI","rain","area"]]
print(column)
fire = fire[column]

fire.reset_index(drop = True,inplace = True)
NewMax = 10
NewMin = 1
OldMin = fire['DMC'].min()
OldMax = fire['DMC'].max()


"""bringing data to range accoring to the formula"""
for i in range(len(fire.index)):
    fire.at[i,'DMC'] = int((((fire.at[i,'DMC'] - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
    #fire.at[i,'area'] = math.log(fire.at[i,'area'])
    fire.at[i,'Ffdi'] = calcFfdi(fire.at[i,'DMC'],fire.at[i,'temp'],fire.at[i,'RH'],fire.at[i,'wind'])
fires = fire.sort_values('Ffdi', ascending = False) 
fires.reset_index(drop = True,inplace = True)
i = 0
pop2 = []
while len(currentPopulation) != 200:
    x = list(fires.loc[i].values)
    if x not in pop2:
        pop2.append(x)
        currentPopulation.append(x)
    i+=1   

print("Initial length of population -",len(currentPopulation))  


'''making the range of the mutation'''
AllMinMax = [[fires['DMC'].min(),fires['DMC'].max()],[fires['temp'].min(),fires['temp'].max()],[fires['RH'].min(),fires['RH'].max()],[fires['wind'].min(),fires['wind'].max()]]



#for i in range(5):

startGenetic(1000,10)
  





