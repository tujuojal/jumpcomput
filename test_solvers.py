

import random
import StringIO
import numpy
import lentoODE
import lento2
import inrunODE
import inrun4
import land
import inter

import numpy as np
import pylab

def testi():
    irODE=inrunODE.Inrun()
    irODE.steps=100
    irODE.ratkaise()
    kodeODE=irODE.takeoff2()
    leODE=lentoODE.Lento(irODE.sx[kodeODE],irODE.sy[kodeODE],irODE.vx[kodeODE],irODE.vy[kodeODE])
    leODE.steps=30
    leODE.ratkaise(irODE.sx[kodeODE],irODE.sy[kodeODE],irODE.vx[kodeODE],irODE.vy[kodeODE])
    pylab.plot(leODE.sx,leODE.sy,color='green')
    pylab.plot(irODE.sx[:kodeODE+1],irODE.sy[:kodeODE+1],color='green')

    irStep=inrun4.Inrun()
    irStep.steps=7000
    irStep.inrun()
    kodeStep=irStep.takeoff2()
    le4=lento2.Lento(irStep.sx[kodeStep],irStep.sy[kodeStep],irStep.vx[kodeStep],irStep.vy[kodeStep])
    le4.steps=2000
    le4.laske(irStep.sx[kodeStep],irStep.sy[kodeStep],irStep.vx[kodeStep],irStep.vy[kodeStep])
    pylab.plot(le4.sx,le4.sy)
    pylab.plot(irStep.sx[:kodeStep+1],irStep.sy[:kodeStep+1])
    pylab.show()

if __name__ == '__main__':
    testi()
