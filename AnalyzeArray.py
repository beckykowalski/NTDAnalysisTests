import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import csv
from sklearn.linear_model import LinearRegression
import re
import DeltaModeErrors
from DeltaModeErrors import *

# datafile: csv file with syntax: Voltage,VoltageError,Temperature,TemperatureError
      #### if data file is not in this format, will need to augment function PARSEDATA
      #### units of Volts are in V, units of Temperature are in K (will need to convert to these units if data is saved in mV or mK)
# current: constant current supplied by test setup
# length: length where current flows across NTD (for R0 calculation)
# width: width of NTD (for R0 calculation)
# height: height of NTD (for R0 calculation)
# instused: string input of options: DMM, DeltaMode, Lakeshore (for error bar calculation)
# cutoff: if there is a temperature cutoff (want to exclude a saturation of temperature for example), provide value

def oneoverx2(x):
    return 1./(x*x/1000.)
def inv(x):
    return 1./np.sqrt(x/1000.)

def PARSEDATA(datafile):

    volt = []
    voltErr = []
    temp = []
    tempErr = []

    
    with open(datafile, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
#            if row[0] == "Still Power (mW)":
            if row[0] == "Volt":
                continue
            vval = float(row[5])*.001
            volt.append(vval)
            voltErr.append(float(row[6])*0.001)
            temp.append(float(row[3])*0.001)
            tempErr.append(float(row[4])*0.001)
    return volt, voltErr, temp, tempErr
    
            
def MakeLNRVSQRTT(datafile, current, length, width, height, instused, currRange, voltRange, cutoff=0):

#    curr = 5 * 10.**-9.

    logres = []
    xfit = []
    yfit = []
    tsqrt = []
    
    volt, vE, temp, tempE = PARSEDATA(datafile)
    for v in volt:
        R = v/current
        logres.append(np.log(R))
    for t in temp:
        tsqrt.append(1./np.sqrt(t))

    if cutoff != 0:
        for i in range(len(temp)):
            if temp[i] > cutoff*0.001:
                xfit.append(1./np.sqrt(temp[i]))
                yfit.append(np.log(volt[i]/current))

#    fig, ax = plt.subplots(constrained_layout=True)
#    ax.scatter(tsqrt,logres)
#    ax.set_xlabel("$ 1/ \sqrt{T} $ [$ K^{1/2} $]")
#    ax.set_ylabel("ln(R) [ln( $\Omega $)]")

    # to get second x axis with temp on top of 
#    sax = ax.secondary_xaxis('top', functions=(oneoverx2, inv))
#    sax.set_xlabel("Temprtature [mK]")
    
#    ticks = np.arange(0,100,20)
    
#    sax.set_xticks(ticks)
    
    xlinear = np.array(xfit).reshape((-1, 1))
#    print(xlinear)
    ylinear = np.array(yfit)
    mod = LinearRegression()
    mod.fit(xlinear, ylinear)
    ypred = mod.predict(xlinear)
#    print("R^2 is "+str(mod.score(xlinear, ylinear)))
#    print("slope is "+str(mod.coef_))
#    print("y intercept is "+str(mod.intercept_))

    return tsqrt, logres, xlinear, ypred, mod.score(xlinear, ylinear), mod.coef_, mod.intercept_

