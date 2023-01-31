import Analyze
from Analyze import *
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import csv
from sklearn.linear_model import LinearRegression
import re


current = 5. * 10. ** -9

PLOTTER_LNRVSQRTT("../Data_Dec11_2022.csv", current, 3., 1., 3., "deltamode", "10nA", "10mV", 37)
