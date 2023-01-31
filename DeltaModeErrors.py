import numpy as np
import scipy as sp


# calculates instrumental uncertainty on: current, voltage, and resistance for
# delta mode nanovoltmeter (Keithley 2182a) and delta mode current source (Keithley 6221)
# values hardcoded come from instrumentation datasheet specifications for accuracy of value at given range
### current source datasheet: https://assets.testequity.com/te1/Documents/pdf/keithley/6220-6221-ds.pdf
### nanovoletmeter datasheet: https://assets.testequity.com/te1/Documents/pdf/keithley/2182A.pdf

# inputs:
## current: single double value in units Amps (set for data aquisition)
## voltage array: list or array of voltage values from data collection in units Volts
## currRange: string for range set when sourcing current during data aquisition
##### options for currRange: 2nA, 20nA, 200nA, 2microA, 20microA, 200microA, 2mA, 20mA, 100mA
## voltRange: string for range set when measuring voltage reading during data aquisition
##### options for voltRange: 10mV, 100mV, 1V, 10V, 100V

# returns: CurrentAccuracy, VoltageAccuracyArray, InstrumentalResistanceUncertaintyArray
##### InstrumentalResistanceUncertaintyAray: sqrt(($delta$I * dR/dI)^2 + ($delta$V * dR/dV)^2 )
##### calculated from partial derivatives of V and I in R = V/I
##### dR/dV = 1/I
##### dR/dI = -(V/I^2)

def DELTAMODEUNCERTAINTY(current, voltagearray, currRange, voltRange):
    CurrentAccuracy = 0.
    if currRange == "2nA":
        CurrentAccuracy = 0.004 * current + .000000000002 # 0.4%_meas + 2pA 
    if currRange == "20nA":
        CurrentAccuracy = 0.003 * current + .00000000001 # 0.3%_meas + 10pA 
    if currRange == "200nA":
        CurrentAccuracy = 0.003 * current + .0000000001 # 0.3%_meas + 100pA 
    if currRange == "2microA":
        CurrentAccuracy = 0.001 * current + .000000001 # 0.1%_meas + 1nA 
    if currRange == "20microA":
        CurrentAccuracy = 0.0005 * current + .00000001 # 0.05%_meas + 10nA 
    if currRange == "200microA":
        CurrentAccuracy = 0.0005 * current + .0000001 # 0.05%_meas + 100nA
    if currRange == "2mA":
        CurrentAccuracy = 0.0005 * current + .000001 # 0.05%_meas + 1microA 
    if currRange == "20mA":
        CurrentAccuracy = 0.0005 * current + .000001 # 0.05%_meas + 1microA 
    if currRange == "100mA":
        CurrentAccuracy = 0.001 * current + .000050 # 0.1%_meas + 50microA 

    VoltageAccuracy = []
    for v in voltagearray:
        # ppm = parts per million: 10ppm = 0.001%
        if voltRange == "10mV":
            VoltageAccuracy.append(v*0.00002+.01*0.000004) # 20ppm*v + 4ppm
        if voltRange == "100mV":
            VoltageAccuracy.append(v*0.00001+.01*0.000003) # 10ppm*v + 3ppm
        if voltRange == "1V":
            VoltageAccuracy.append(v*0.000007+.01*0.000002) # 7ppm*v + 2ppm
        if voltRange == "10V":
            VoltageAccuracy.append(v*0.000002+.01*0.000001) # 2ppm*v + 1ppm
        if voltRange == "100V":
            VoltageAccuracy.append(v*0.00001+.01*0.000003) # 10ppm*v + 3ppm

    ResUncertainty = []
    for v in range(len(voltagearray)):

        VoltageComponent = VoltageAccuracy[v] * (1./current)

        CurrentComponent = CurrentAccuracy * (-1.*voltagearray[v]/(current*current))

        ResUncertaintyVal = np.sqrt(VoltageComponant*VoltageComponant + CurrentComponant*CurrentComponant)
        
        ResUncertainty.append(ResUncertaintyVal)
    return CurrentAccuracy, VoltageAccuracy, ResUncertainty 
            
