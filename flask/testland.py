

#!/usr/bin/python

from scipy import *
import pylab
import land
import lento2

le=lento2.Lento(10,-10,9,20)
la=land.Land(1,10,30,10,le.sx[0],le.sy[0])
hit=la.osu(le)
print hit
pylab.plot(le.sx[:hit],le.sy[:hit],la.xx,la.yy)
pylab.show()

