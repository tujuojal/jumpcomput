
#!/usr/bin/python

from scipy import *
import pylab

class Land:
    def __init__(self,takeheigh=1,length=10,landangle=30,landheight=10,takesx=0,takesy=0):
        """
        muodestetaan simppeli geometria hyppyrille
        """
        self.yy=[takesy-takeheight,takesy-takeheight,takesy-takeheight-landheight]
        self.xx=[takesx,takesx+length,takesx+length+landheight/tan(landangle*pi*2./360.)]

        def osu(self,lento):
            """
            syötetään lentorata ja lasketaan osuuko alastuloon ja millä indeksillä
            """
            for i in range(len(lento.t)-1):
                if lento.sx<self.xx[1] and lento.sy<self.yy[0]
                    return i
                else if

