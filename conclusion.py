import pandas
import xlrd
import math
import statistics as st
import matplotlib.pyplot as plt

def calcFfdi(DF,T,RH, U):
    return int( 2 * math.exp(-0.45 + 0.978*math.log(DF) - 0.0345 * RH + 0.0338 * T + 0.0234 * U))

fire  = pandas.read_excel("BestIndividuals.xlsx")
plt.plot(fire['Generation'],fire['FFDI'])
plt.margins(y=0.1)
plt.xlabel("Generation")
plt.ylabel("FFDI")
plt.show()


xls = pandas.ExcelFile('AllPopulation.xlsx')

low = pandas.read_excel(xls,'Low')
medium = pandas.read_excel(xls,'Medium')
high = pandas.read_excel(xls,'High')



lowMeans = [low['Drought Factor'].mean(),low['Temperature'].mean(),low['Relative Humidity'].mean(),low['Wind'].mean(),low['FFDI'].mean()]
mediumMeans = [medium['Drought Factor'].mean(),medium['Temperature'].mean(),medium['Relative Humidity'].mean(),medium['Wind'].mean(),medium['FFDI'].mean()]
highMeans = [high['Drought Factor'].mean(),high['Temperature'].mean(),high['Relative Humidity'].mean(),high['Wind'].mean(),high['FFDI'].mean()]


mean1 = [st.mean([lowMeans[0],mediumMeans[0]]),st.mean([lowMeans[1],mediumMeans[1]]),st.mean([lowMeans[2],mediumMeans[2]]),st.mean([lowMeans[3],mediumMeans[3]]),st.mean([lowMeans[4],mediumMeans[4]])]
mean2 = [st.mean([mediumMeans[0],highMeans[0]]),st.mean([mediumMeans[1],highMeans[1]]),st.mean([mediumMeans[2],highMeans[2]]),st.mean([mediumMeans[3],highMeans[3]]),st.mean([mediumMeans[4],highMeans[4]])]
print("DF","Temp","RH","Wind","FFDI",sep='\t\t\t')
for item in mean1:
    print(item,end='\t')
print()
for item in mean2:
    print(item,end='  \t')
print()
print("==========ENTER VALUES============")
val = True;
while val :
    DF = input("Enter value for DF:")
    temp = input("Enter value for temp:")
    RH = input("Enter value for RH:")
    Wind = input("Enter value for Wind:")
    ffdi = calcFfdi(float(DF), float(temp), float(RH), float(Wind))

    if ffdi < mean1[-1]:
        print("FFDI is LOW")
    elif ffdi < mean2[-1]:
        print("FFDI is MEDIUM")
    else:
        print("FFDI is HIGH")
    
    ip=input("To insert new values, press \'y\': ")

    if ip != "y":
        break;

