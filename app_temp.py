"Plot a PNG using matplotlib in a web request, using Flask."

# Install dependencies, preferably in a virtualenv:
#
# pip install flask matplotlib
#
# Run the development server:
#
# python app.py
#
# Go to http://localhost:5000/plot.png and see a plot of random data.

import random
import StringIO
import numpy
import lentoODE
import inrunODE
import land
import inter

from flask import Flask, make_response, render_template_string, render_template, url_for, request
from wtforms import Form, SelectMultipleField, DecimalField, FloatField
import matplotlib
matplotlib.use("agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

############################################################
## Data of the computation via WTForm ##
############################################################

class Data(Form):
    friction = FloatField('Friction coeff (0.02-0.06 maybe?)',default=0.05)
    airdrag = FloatField('Airdrag const', default=0.4)
    radius = FloatField('Radius of tranny',default=25)
    radius2 = FloatField('Radius of tranny nr2',default=20)
    angle = FloatField('Angle of inrun',default=24)
    takeangle = FloatField('Angle of takeof',default=20)
    flat = FloatField('Length of inrun-flat',default=5)
    height = FloatField('Height of Inrun',default=24)
    takeheight = FloatField('Height of Takeoff',default=4)
    desitime = FloatField('Hangtime',default=2)
    landlength = FloatField('Length of table', default = 10)
    landangle = FloatField('Angle of landing', default = 24)
    landheight = FloatField('Height of landing', default =20)
    landdrop = FloatField('Drop from takeof', default = 1)

###########################################################
## Templates for the html as filled and so ##
###########################################################

template_form = """

"""

#########################################################
## and the other template... ##
#########################################################

completed_template = """


"""


###########################################################################
## now the application itself ############
###########################################

app = Flask(__name__)

def init():
    """"initializing the computations and calling the template"""
    app.ir=inrunODE.Inrun()
    app.ir.C=0.05
    app.ir.D=0.4
    app.ir.A=app.ir.D/app.ir.m
    app.ir.ratkaise()
    app.kode=app.ir.takeoff2()
    app.lent=lentoODE.Lento(app.ir.sx[app.kode],app.ir.sy[app.kode],app.ir.vx[app.kode],app.ir.vy[app.kode])
    app.lent.D=0.4
    app.lent.A=app.lent.D/app.lent.m
    app.alast=land.Land(takeheight=1,length=10,landangle=30,landheight=10,takesx=app.ir.sx[app.kode],takesy=app.ir.sy[app.kode])
    app.osuma=app.alast.osu(app.lent)
    #app.form.desitime.data=app.
    print app.lent.t[app.osuma]
    print "osuma-aika"

    """"initializing the computations for smaller speed and calling the template"""
    app.lista=[0.9,1.1]
    app.ir2=inrunODE.Inrun()
    app.ir2.C=0.05
    app.ir2.D=0.4
    app.ir2.A=app.ir2.D/app.ir2.m
    app.ir2.ratkaise()
    app.kode2=app.ir2.takeoff2()
    app.lent2=lentoODE.Lento(app.ir.sx[app.kode],app.ir.sy[app.kode],app.ir2.vx[app.kode2],app.ir2.vy[app.kode2])
    app.lent2.D=0.4
    app.lent2.A=app.lent2.D/app.lent2.m
    app.alast2=land.Land(takeheight=1,length=10,landangle=30,landheight=10,takesx=app.ir.sx[app.kode],takesy=app.ir.sy[app.kode])
    app.osuma2=app.alast2.osu(app.lent2)

@app.route("/", methods=['GET','POST'])
def simple():
    app.form = Data(request.form)
    init()
    if request.method == 'POST':
        radius = request.form['radius']
        print radius
        print "tassa on se radius--------------------------------"
        return render_template('completed_template.html', form=app.form)

    else:
        return render_template('template_form.html', form=app.form)

##################################################
## This is the default computation ##
##################################################

@app.route('/plot.png')
def plot(angle=24., ylengthstr=24.,  radius=25.,radius2=20., flat=4,takeoffAngle=20.*2.*numpy.pi/360., takeoffHeight=4.):
    app.fig = Figure()
    app.axis = app.fig.add_subplot(1, 1, 1)

# remove computations into some auxiliary function and just loop the plot here
# to test, lets make only three
    app.ir.ylengthstr=ylengthstr
    app.ir.runangle=angle*2.*numpy.pi/360.
    app.ir.radius=radius
    app.ir.radius2=radius2
    app.ir.flat=flat
    app.ir.takeoffAngle=takeoffAngle
    app.ir.takeoffHeight=takeoffHeight


    app.ir.ratkaise()
    app.kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[app.kode]
    syloppu=app.ir.sy[app.kode]
    vxloppu=app.ir.vx[app.kode]
    vyloppu=app.ir.vy[app.kode]

    app.lent.ratkaise(sxloppu,syloppu,vxloppu,vyloppu)
    app.alast.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sxloppu,syloppu)
    app.osuma=app.alast.osu(app.lent)
    print "Osumakohtiaaaa!!"
    print app.osuma
    app.form.desitime.data=app.lent.t[app.osuma]
    print app.form.desitime.data

# there is time 4.5sec in lentoODE
# dt is the size of timestep so to reach desiredtime go to step desiredtime/dt
# by default desiredtime =2
    xs = app.lent.sx
    ys = app.lent.sy

# This is the other step of the loop, with added friction and airdrag...

    scatterlist=[[]] #this is empty list that will get added within the loop
    for i in app.lista:
        app.ir2.ylengthstr=ylengthstr
        app.ir2.runangle=angle*2.*numpy.pi/360.
        app.ir2.radius=radius
        app.ir2.radius2=radius2
        app.ir2.flat=flat
        app.ir2.takeoffAngle=takeoffAngle
        app.ir2.takeoffHeight=takeoffHeight

        app.ir2.C=0.05*i
        app.ir2.D=0.4*i
        app.ir2.A=app.ir2.D/app.ir2.m

        app.ir2.ratkaise()
        app.kode2=app.ir2.takeoff2()

        app.lent2.D=0.4*i
        app.lent2.A=app.lent2.D/app.lent2.m

        sx2loppu=app.ir.sx[app.kode]
        sy2loppu=app.ir.sy[app.kode]
        vx2loppu=app.ir2.vx[app.kode2]
        vy2loppu=app.ir2.vy[app.kode2]

        app.lent2.ratkaise(sx2loppu,sy2loppu,vx2loppu,vy2loppu)
        app.alast2.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sx2loppu,sy2loppu)
        app.osuma2=app.alast2.osu(app.lent2)
        print "Osumakohtiaaaa!!"
        print app.osuma2
        app.form.desitime.data=app.lent2.t[app.osuma]
        print app.form.desitime.data

# there is time 4.5sec in lentoODE
# dt is the size of timestep so to reach desiredtime go to step desiredtime/dt
# by default desiredtime =2
        xs2 = app.lent2.sx
        ys2 = app.lent2.sy
# loop should go through the number of flightpaths
       # colorcode=inter.osumavoima(app.osuma2,app.lent2,app.alast2)
       # scatterlist.append([xs2[app.osuma2],ys2[app.osuma2],colorcode])
        app.axis.plot(xs2[:app.osuma2+1], ys2[:app.osuma2+1],color="green",linewidth=1)
   # colorcode=inter.osumavoima(app.osuma,app.lent,app.alast)
   # scatterlist.append([xs[app.osuma],ys[app.osuma],colorcode])
   # app.axis.scatter(scatterlist[1],scatterlist[2],s=10,c=scatterlist[3])
    app.axis.plot(xs[:app.osuma+1], ys[:app.osuma+1],color="red",linewidth=2,label="flightpath")
    app.axis.plot(app.ir.sx[:app.kode+1], app.ir.sy[:app.kode+1], color="black" , linewidth=1, label = "kicker")
    app.axis.plot(app.alast.xx, app.alast.yy, color="black" , linewidth=1, label = "kicker")
#    app.axis.fill_between(app.ir.sx[:app.kode], -40, app.ir.sy[:app.kode], color="black" )
#This is the thing to plot colors according the impact:
#cmhot = app.axis.plot.cm.get_cmap("hot")
#app.axis.scatter(osumax,osumay,c=varikoodi,cmap=cmhot)
#Not quite sure if the above is corect, also inter.py which should
#compute the impacts is very unproven..."
    app.axis.legend(loc='upper right')
    app.canvas = FigureCanvas(app.fig)
    app.output = StringIO.StringIO()
    app.canvas.print_png(app.output)
    app.response = make_response(app.output.getvalue())
    app.response.mimetype = 'image/png'
    return app.response

####################################################
## This will be the recomputation with parameters ##
####################################################

@app.route('/replot.png')
def replot(angle=25., ylengthstr=20., radius=20., flat=5,takeoffAngle=20.*2.*numpy.pi/360., takeoffHeight=4.):
    app.fig = Figure()
    app.axis = app.fig.add_subplot(1, 1, 1)
    app.ir.C=app.form.friction.data
    app.ir.D=app.form.airdrag.data
    app.ir.A=app.ir.D/app.ir.m
    app.lent.D=app.form.airdrag.data
    app.lent.A=app.lent.D/app.lent.m
    app.ir.ylengthstr=app.form.height.data
    app.ir.runangle=app.form.angle.data*2.*numpy.pi/360.
    app.ir.radius=app.form.radius.data
    app.ir.radius2=app.form.radius2.data
    app.ir.flat=app.form.flat.data
    app.ir.takeoffAngle=app.form.takeangle.data*2.*numpy.pi/360.
    app.ir.takeoffHeight=app.form.takeheight.data


    app.ir.ratkaise()
    app.kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[app.kode]
    syloppu=app.ir.sy[app.kode]
    vxloppu=app.ir.vx[app.kode]
    vyloppu=app.ir.vy[app.kode]

    app.lent.ratkaise(sxloppu,syloppu,vxloppu,vyloppu)
    app.alast.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sxloppu,syloppu)
    app.osuma=app.alast.osu(app.lent)

    print "Hang time hang time...!!"
    print app.osuma
    app.form.desitime.data=app.lent.t[app.osuma]

    # there is time 4.5sec in lentoODE
# dt is the size of timestep so to reach desiredtime go to step desiredtime/dt
# by default desiredtime =2
    xs = app.lent.sx
    ys = app.lent.sy

    app.axis.plot(xs[:app.osuma+1], ys[:app.osuma+1],color="red",linewidth=2,label="flightpath")
    app.axis.plot(app.ir.sx[:app.kode+1], app.ir.sy[:app.kode+1], color="black" , linewidth=1, label = "kicker")
    app.axis.plot(app.alast.xx, app.alast.yy, color="black" , linewidth=1, label = "kicker")

# This is the other step of the loop, with added friction and airdrag...

    app.ir2.ylengthstr=app.form.height.data
    app.ir2.runangle=app.form.angle.data*2.*numpy.pi/360.
    app.ir2.radius=app.form.radius.data
    app.ir2.radius2=app.form.radius2.data
    app.ir2.flat=app.form.flat.data
    app.ir2.takeoffAngle=app.form.takeangle.data*2.*numpy.pi/360.
    app.ir2.takeoffHeight=app.form.takeheight.data
    for i in app.lista:

        app.ir2.C=app.form.friction.data*i
        app.ir2.D=app.form.airdrag.data*i
        app.ir2.A=app.ir2.D/app.ir2.m

        app.ir2.ratkaise()
        app.kode2=app.ir2.takeoff2()

        app.lent2.D=app.form.airdrag.data*i
        app.lent2.A=app.lent2.D/app.lent2.m

        sx2loppu=app.ir.sx[app.kode]
        sy2loppu=app.ir.sy[app.kode]
        vx2loppu=app.ir2.vx[app.kode2]
        vy2loppu=app.ir2.vy[app.kode2]

        app.lent2.ratkaise(sx2loppu,sy2loppu,vx2loppu,vy2loppu)
        app.alast2.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sx2loppu,sy2loppu)
        app.osuma2=app.alast2.osu(app.lent2)
        print "Osumakohtiaaaa!!"
        print app.osuma2
        app.form.desitime.data=app.lent2.t[app.osuma2]
        print app.form.desitime.data

        xs2 = app.lent2.sx
        ys2 = app.lent2.sy
        app.axis.plot(xs2[:app.osuma2+1], ys2[:app.osuma2+1],color="green",linewidth=1)
#-------------------------------------------------------------------
#-------------------------------------------------------------------
    app.axis.legend(loc='upper right')
    app.canvas = FigureCanvas(app.fig)
    app.output = StringIO.StringIO()
    app.canvas.print_png(app.output)
    app.response = make_response(app.output.getvalue())
    app.response.mimetype = 'image/png'
    return app.response


if __name__ == '__main__':
    app.run(debug=True)

