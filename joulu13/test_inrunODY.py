import pylab
import inrunODE
import time
lasku = inrunODE.Inrun()
t0=time.clock()
ratk=lasku.ratkaise()
t1=time.clock() - t0
print "ODEint ratkaisijalla:" + str(t1)

"""
t2=time.clock() 
lasku.inrun()
t3=time.clock() - t2
print "eteenpain steppaavalla:" + str(t3)
"""

t4=time.clock() 
lasku.takeoff2()
t5=time.clock() - t4
print "nokan hakemiseen:" + str(t5)

u=ratk.T
pylab.plot(u[2],u[3],'r',lasku.sx,lasku.sy)
pylab.show()
