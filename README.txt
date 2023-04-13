To run:

Only thing that should need to be edited is RunAnalyze.py

# in datafiles: every list inside the list of lists is syntax:
  ["path to data file for NTD", "name of NTD", <AreaCurrentSentThroughNTD/LenghtCurrentSentThroughNTD>]


This should take N datafiles for N different NTDs inside the list "datafiles" to:
     # plot all NTDs, data as a scatter and linear regression fit as a line
     ### plot is of lnR vs sqrt(T0/T)
     ### top of plot should be in units of T
     # make an output text file of fit information
       Spits out R0/T0, chi2 of fit, and fit parameters in linear model 

Datafiles should have units of:
     # miliKelvin for temp
     # miliVolts for voltage
     ### convert from these units to normal Volts and Kelvin in PARSEDATA in AnalyzeArray.py
