


#!/usr/bin/python


import scipy.interpolate as interpolate
import scipy.optimize as optimize
import numpy as np
import pylab

def osuma(lento,alastulo):
    xx2=np.array(range(len(alastulo.xx)))
    yy2=np.array(range(len(alastulo.yy)))
    for i in range(len(alastulo.xx)):
        xx2[i]=alastulo.xx[i]
        yy2[i]=alastulo.yy[i]
    p2=interpolate.PiecewisePolynomial(xx2,yy2[:,np.newaxis])
    for val in range(len(lento.sy)):
        if lento.sy[val]<p2(lento.sx[val]):
            print "ONNISTUU!!:"
            return i
    return len(lento.sx)
