


#!/usr/bin/python


import scipy.interpolate as interpolate
import scipy.optimize as optimize
import numpy as np
import pylab

def osuma(lento,alastulo):
    xx2=np.array(range(len(alastulo)))
    yy2=np.array(range(len(alastulo)))
    for i in range(len(alastulo)):
        xx2[i]=alastulo[i][0]
        yy2[i]=alastulo[i][1]
    p2=interpolate.PiecewisePolynomial(xx2,yy2[:,np.newaxis])
    for val in range(len(lento)):
        if lento[i][1]<p2(lento[i][0]):
            return i
    return len(lento)
