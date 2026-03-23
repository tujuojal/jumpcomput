


#!/usr/bin/python

import matplotlib
matplotlib.use("agg")
import scipy.interpolate as interpolate
import scipy.optimize as optimize
import numpy as np
import pylab

def osuma(lento,alastulo):
    xx2=np.array(alastulo.xx,dtype=float)
    yy2=np.array(alastulo.yy,dtype=float)
    p2=interpolate.CubicSpline(xx2,yy2)
    for val in range(len(lento.sy)):
        if lento.sy[val]<p2(lento.sx[val]):
            print "ONNISTUU!!:"
            return val
    return len(lento.sx)

def osumavoima(osumakohta,lento,alastulo):
    xx2=np.array(alastulo.xx,dtype=float)
    yy2=np.array(alastulo.yy,dtype=float)
    p2=interpolate.CubicSpline(xx2,yy2)
    kulma=p2.derivative()(lento.sx)  #this is list of the first derivatives at points of flightpath
    isku=(lento.vx[osumakohta]*kulma[osumakohta]+lento.vy[osumakohta])/np.sqrt(kulma[osumakohta]*kulma[osumakohta]+1)
    return isku
