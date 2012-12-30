


#!/usr/bin/python


import scipy.interpolate as interpolate
import scipy.optimize as optimize
import numpy as np
import pylab

def osuma(lento,alastulo):
    xx2=np.array(alastulo.xx,dtype=float)
    yy2=np.array(alastulo.yy,dtype=float)
    p2=interpolate.PiecewisePolynomial(xx2,yy2[:,np.newaxis])
    for val in range(len(lento.sy)):
        if lento.sy[val]<p2(lento.sx[val]):
            print "ONNISTUU!!:"
            return i
    return len(lento.sx)
