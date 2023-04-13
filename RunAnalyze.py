import AnalyzeArray
from AnalyzeArray import *
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import csv
from sklearn.linear_model import LinearRegression
import re

def oneoverx2(x):
    return 1./(x*x/1000.)
def inv(x):
    return 1./np.sqrt(x/1000.)

current = 5. * 10. ** -9

datafiles = [["../Data_Dec11_2022.csv", "3x3x1", 3.*1./3.], ["../Data_Dec11_2022_testing.csv", "3x1x1", 1.*1./3], ["", "3x0.5x1", 0.5*1./3.], ["", "1x1x1", 1.*1./1.]]

outfile = open("NTD_Characteristics.txt", "w")
count = 0

fig, ax = plt.subplots(constrained_layout = True)
ax.set_xlabel("$ 1/ \sqrt{T} $ [$ K^{1/2} $]")
ax.set_ylabel("ln(R) [ln( $\Omega $)]")

# to get second x axis with temp on top of
sax = ax.secondary_xaxis('top', functions=(oneoverx2, inv))
sax.set_xlabel("Temprtature [mK]")
ticks = np.arange(0,100,20)
sax.set_xticks(ticks)

temp331, res331, x331, y331, chi331, m331, b331 = MakeLNRVSQRTT("../Data_Dec11_2022.csv", current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)
temp311, res311, x311, y311, chi311, m311, b311 = MakeLNRVSQRTT("../Data_Dec11_2022_testing.csv", current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)
temp351, res351, x351, y351, chi351, m351, b351 = MakeLNRVSQRTT("../Data_Dec11_2022_testing.csv", current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)
temp111, res111, x111, y111, chi111, m111, b111 = MakeLNRVSQRTT("../Data_Dec11_2022_testing.csv", current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)

plt.scatter(temp331, res331, label="3x3x1 Data")
plt.plot(x331, y331, label='3x3x1 Fit')
plt.scatter(temp311, res311, label="3x1x1 Data")
plt.plot(x311, y311, label='3x1x1 Fit')
#plt.scatter(temp351, res351, label="3x0.5x1 Data")
#plt.plot(x351, y351, label='3x0.5x1 Fit')
#plt.scatter(temp111, res111, label="1x1x1 Data")
#plt.plot(x111, y111, label='1x1x1 Fit')

plt.legend(loc='best')

plt.savefig("allNTDs.png")

for data in datafiles:
    count = count + 1
    if count < 3:
        temp, res, x, y, chi, m, b = MakeLNRVSQRTT(data[0], current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)
        print("y intercept is "+str(b))
        outfile.write(data[1] + " NTD: y = "+str(round(m[0], 2))+"x + "+str(round(b, 2))+"\n")
        # NTD model of resistivity is: rho(T) = rho0 * exp(sqrt[T0/T])
        ### or ln[rho(T) = ln[rho0] + sqrt[T0/T]
        # gets R0 by taking exponential of y intercept (b) multiplying by Lenght/Area of current applied through NTD (rho = RA/L)
        # gets T0 by taking squre of slope (m)
        outfile.write(data[1] + " NTD: R0 = "+str((np.exp(b) / data[2]))+" ohms, T0 = "+str(m[0]*m[0])+"\n")
        outfile.write(data[1] + " NTD Fit quality: chi2 = "+str(chi))

outfile.close()
