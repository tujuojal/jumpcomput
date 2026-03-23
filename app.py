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

import os
import StringIO
import numpy
import lentoODE
import inrunODE
import land
import inter

from flask import Flask, make_response, render_template_string, url_for, request, session
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

<title>Computatio</title>

<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
<div class=page>
  <h1>Computatio</h1>

  <p> This is a testsite for computations for kickers. Updates are coming.... </p>
  <p> Dec19/2013 -- Now added extra flightpaths to indicate mistake in airdrag coefficient and friction coefficient
  up to 10%. Maybe this helps to understand the uncertainty of the result.</p>
  <p> Apr11/2014 -- Just for a change now, this uses the scipy.integrate.odeint to solve the ode </p>
  <p> Friction is taken into account by multiplying the support force by friction coefficient, the inrun is being drawn as
  the path determined by the forces which are determined by the parameters. So, in principle you should be able to see the
  numerical error when it is big. </p>
  <p> Airresistance is quadratic wrt speed, default coefficient is set to correspond some windtunnel tests for crosscountry
  <a href = "http://biomekanikk.nih.no/xchandbook/ski4.html"> skiers! </a> </p>
  <p>See
  <a href="http://users.jyu.fi/~tujuojal/harrasteosio.html"> my website </a> and info there about this project.
  </p>
    <div class=img>
        <img src="{{ url_for('plot') }}" height="80%" width="100%" alt="Wait... computing in process...">
    </div>

{% block content %}
<h1>Set the parameters</h1>

<form method="POST" action="/">
    <div>{{ form.friction.label }} {{ form.friction() }}</div>
    <div>{{ form.airdrag.label }} {{ form.airdrag() }}</div>
    <div>{{ form.radius.label }} {{ form.radius() }}</div>
    <div>{{ form.radius2.label }} {{ form.radius2() }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }}</div>
    <div>{{ form.flat.label }} {{ form.flat() }} </div>
    <div>{{ form.height.label }} {{ form.height() }} </div>
    <div>{{ form.takeheight.label }} {{ form.takeheight() }} </div>
    <div>{{ form.takeangle.label }} {{ form.takeangle() }} </div>
    <div>{{ form.landlength.label }} {{ form.landlength() }} </div>
    <div>{{ form.landangle.label }} {{ form.landangle() }} </div>
    <div>{{ form.landheight.label }} {{ form.landheight() }} </div>
    <div>{{ form.landdrop.label }} {{ form.landdrop() }} </div>
    <button type="submit" class="btn">Submit</button>
</form>

{% endblock %}

"""

#########################################################
## and the other template... ##
#########################################################

completed_template = """

<title>Computatio</title>

<link rel=stylesheet type=text/css href="{{ url_for('static', filename='default.css') }}">

  <p> This is a testsite for computations for kickers. Updates are coming.... </p>
  <p> Dec19/2013 -- Now added extra flightpaths to indicate mistake in airdrag coefficient and friction coefficient
  up to 10%. Maybe this helps to understand the uncertainty of the result.</p>
  <p> Friction is taken into account by multiplying the support force by friction coefficient, the inrun is being drawn as
  the path determined by the forces which are determined by the parameters. So, in principle you should be able to see the
  numerical error when it is big. </p>
  <p> Airresistance is quadratic wrt speed, coefficient is set to correspond some windtunnel tests for crosscountry
  <a href = "http://biomekanikk.nih.no/xchandbook/ski4.html"> skiers! </a> </p>
  <p>See
  <a href="http://users.jyu.fi/~tujuojal/harrasteosio.html"> my website </a> and info there about this project.
  </p>
    <div class=img>
        <img src="{{ url_for('replot') }}" height="80%" width="100%" alt="Computing in process... Wait.. wait...">
    </div>

{% block content %}
<h1>Data selected</h1>
<form method="POST" action="/">
    <div>{{ form.friction.label }} {{ form.friction() }} {{ form.friction.data }}</div>
    <div>{{ form.airdrag.label }} {{ form.airdrag() }} {{ form.airdrag.data }}</div>
    <div>{{ form.radius.label }} {{ form.radius() }} {{ form.radius.data }}</div>
    <div>{{ form.radius2.label }} {{ form.radius2() }} {{ form.radius2.data }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }} {{ form.angle.data }}</div>
    <div>{{ form.takeangle.label }} {{ form.takeangle() }} {{ form.takeangle.data }}</div>
    <div>{{ form.flat.label }} {{ form.flat() }} {{ form.flat.data }}</div>
    <div>{{ form.height.label }} {{ form.height() }} {{ form.height.data }}</div>
    <div>{{ form.takeheight.label }} {{ form.takeheight() }} {{ form.takeheight.data }}</div>
    <div>{{ form.landlength.label }} {{ form.landlength() }} {{ form.landlength.data }}</div>
    <div>{{ form.landangle.label }} {{ form.landangle() }} {{ form.landangle.data }}</div>
    <div>{{ form.landheight.label }} {{ form.landheight() }} {{ form.landheight.data }}</div>
    <div>{{ form.landdrop.label }} {{ form.landdrop() }} {{ form.landdrop.data }}</div>
    <button type="submit" class="btn">Submit</button>
    </form>
{% endblock %}

"""


###########################################################################
## now the application itself ############
###########################################

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'jumpcomput-change-this-secret-in-production')

# Scaling factors for uncertainty band (±10% on friction and airdrag)
lista = [0.9, 1.1]

@app.route("/", methods=['GET','POST'])
def simple():
    form = Data(request.form)
    if request.method == 'POST':
        # Store submitted form values in session so /replot.png can read them
        session['form_data'] = {
            'friction':   form.friction.data,
            'airdrag':    form.airdrag.data,
            'radius':     form.radius.data,
            'radius2':    form.radius2.data,
            'angle':      form.angle.data,
            'takeangle':  form.takeangle.data,
            'flat':       form.flat.data,
            'height':     form.height.data,
            'takeheight': form.takeheight.data,
            'landlength': form.landlength.data,
            'landangle':  form.landangle.data,
            'landheight': form.landheight.data,
            'landdrop':   form.landdrop.data,
        }
        return render_template_string(completed_template, form=form)
    else:
        return render_template_string(template_form, form=form)

##################################################
## This is the default computation ##
##################################################

@app.route('/plot.png')
def plot(angle=24., ylengthstr=24., radius=25., radius2=20., flat=4,
         takeoffAngle=20.*2.*numpy.pi/360., takeoffHeight=4.):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    ir = inrunODE.Inrun()
    ir.C = 0.05
    ir.D = 0.4
    ir.A = ir.D / ir.m
    ir.ylengthstr = ylengthstr
    ir.runangle = angle * 2. * numpy.pi / 360.
    ir.radius = radius
    ir.radius2 = radius2
    ir.flat = flat
    ir.takeoffAngle = takeoffAngle
    ir.takeoffHeight = takeoffHeight
    ir.ratkaise()
    kode = ir.takeoff2()

    sxloppu = ir.sx[kode]
    syloppu = ir.sy[kode]
    vxloppu = ir.vx[kode]
    vyloppu = ir.vy[kode]

    lent = lentoODE.Lento(sxloppu, syloppu, vxloppu, vyloppu)
    lent.D = 0.4
    lent.A = lent.D / lent.m
    alast = land.Land(takeheight=1, length=10, landangle=24, landheight=20,
                      takesx=sxloppu, takesy=syloppu)
    osuma_idx = inter.osuma(lent, alast)
    print lent.t[osuma_idx]
    print "osuma-aika"

    xs = lent.sx
    ys = lent.sy

    scatterlist = [[]]
    for i in lista:
        ir2 = inrunODE.Inrun()
        ir2.ylengthstr = ylengthstr
        ir2.runangle = angle * 2. * numpy.pi / 360.
        ir2.radius = radius
        ir2.radius2 = radius2
        ir2.flat = flat
        ir2.takeoffAngle = takeoffAngle
        ir2.takeoffHeight = takeoffHeight
        ir2.C = 0.05 * i
        ir2.D = 0.4 * i
        ir2.A = ir2.D / ir2.m
        ir2.ratkaise()
        kode2 = ir2.takeoff2()

        lent2 = lentoODE.Lento(ir2.sx[kode2], ir2.sy[kode2],
                                ir2.vx[kode2], ir2.vy[kode2])
        lent2.D = 0.4 * i
        lent2.A = lent2.D / lent2.m
        alast2 = land.Land(takeheight=1, length=10, landangle=24, landheight=20,
                           takesx=ir2.sx[kode2], takesy=ir2.sy[kode2])
        osuma2_idx = inter.osuma(lent2, alast2)
        print "Osumakohtiaaaa!!"
        print osuma2_idx

        xs2 = lent2.sx
        ys2 = lent2.sy
        axis.plot(xs2[:osuma2_idx+1], ys2[:osuma2_idx+1], color="green", linewidth=1)

    axis.plot(xs[:osuma_idx+1], ys[:osuma_idx+1], color="red", linewidth=2, label="flightpath")
    axis.plot(ir.sx[:kode+1], ir.sy[:kode+1], color="black", linewidth=1, label="kicker")
    axis.plot(alast.xx, alast.yy, color="black", linewidth=1, label="kicker")
    axis.legend(loc='upper right')
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

####################################################
## This will be the recomputation with parameters ##
####################################################

@app.route('/replot.png')
def replot():
    # Read form data saved to session by the POST to /
    fd = session.get('form_data', {})
    friction   = fd.get('friction',   0.05)
    airdrag    = fd.get('airdrag',    0.4)
    radius     = fd.get('radius',     25.)
    radius2    = fd.get('radius2',    20.)
    angle      = fd.get('angle',      24.)
    takeangle  = fd.get('takeangle',  20.)
    flat       = fd.get('flat',       5.)
    height     = fd.get('height',     24.)
    takeheight = fd.get('takeheight', 4.)
    landlength = fd.get('landlength', 10.)
    landangle  = fd.get('landangle',  24.)
    landheight = fd.get('landheight', 20.)
    landdrop   = fd.get('landdrop',   1.)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    ir = inrunODE.Inrun()
    ir.C = friction
    ir.D = airdrag
    ir.A = ir.D / ir.m
    ir.ylengthstr = height
    ir.runangle = angle * 2. * numpy.pi / 360.
    ir.radius = radius
    ir.radius2 = radius2
    ir.flat = flat
    ir.takeoffAngle = takeangle * 2. * numpy.pi / 360.
    ir.takeoffHeight = takeheight
    ir.ratkaise()
    kode = ir.takeoff2()

    sxloppu = ir.sx[kode]
    syloppu = ir.sy[kode]
    vxloppu = ir.vx[kode]
    vyloppu = ir.vy[kode]

    lent = lentoODE.Lento(sxloppu, syloppu, vxloppu, vyloppu)
    lent.D = airdrag
    lent.A = lent.D / lent.m
    alast = land.Land(takeheight=landdrop, length=landlength, landangle=landangle,
                      landheight=landheight, takesx=sxloppu, takesy=syloppu)
    osuma_idx = inter.osuma(lent, alast)

    print "Hang time hang time...!!"
    print osuma_idx

    xs = lent.sx
    ys = lent.sy

    axis.plot(xs[:osuma_idx+1], ys[:osuma_idx+1], color="red", linewidth=2, label="flightpath")
    axis.plot(ir.sx[:kode+1], ir.sy[:kode+1], color="black", linewidth=1, label="kicker")
    axis.plot(alast.xx, alast.yy, color="black", linewidth=1, label="kicker")

    for i in lista:
        ir2 = inrunODE.Inrun()
        ir2.ylengthstr = height
        ir2.runangle = angle * 2. * numpy.pi / 360.
        ir2.radius = radius
        ir2.radius2 = radius2
        ir2.flat = flat
        ir2.takeoffAngle = takeangle * 2. * numpy.pi / 360.
        ir2.takeoffHeight = takeheight
        ir2.C = friction * i
        ir2.D = airdrag * i
        ir2.A = ir2.D / ir2.m
        ir2.ratkaise()
        kode2 = ir2.takeoff2()

        lent2 = lentoODE.Lento(ir2.sx[kode2], ir2.sy[kode2],
                                ir2.vx[kode2], ir2.vy[kode2])
        lent2.D = airdrag * i
        lent2.A = lent2.D / lent2.m
        alast2 = land.Land(takeheight=landdrop, length=landlength, landangle=landangle,
                           landheight=landheight, takesx=ir2.sx[kode2], takesy=ir2.sy[kode2])
        osuma2_idx = inter.osuma(lent2, alast2)
        print "Osumakohtiaaaa!!"
        print osuma2_idx

        xs2 = lent2.sx
        ys2 = lent2.sy
        axis.plot(xs2[:osuma2_idx+1], ys2[:osuma2_idx+1], color="green", linewidth=1)

    axis.legend(loc='upper right')
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == '__main__':
    app.run()
