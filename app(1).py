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
import lento2
import inrun4
import land
import inter

from flask import Flask, make_response, render_template_string, url_for, request
from wtforms import Form, SelectMultipleField, DecimalField, FloatField
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

<link rel=stylesheet type=text/css href="{{ url_for('static', filename='default.css') }}">

  <p> This is a testsite for computations for kickers. Updates are coming.... </p>
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
  <P> Friction is taken into account by multiplying the support force by friction coefficient, the inrun is being drawn as
  the path determined by the forces which are determined by the parameters. So, in principle you should be able to see the
  numerical error when it is big. </p>
  <p> Airreisistance is quadratic wrt speed, coefficient is set to correspond some windtunnel tests for crosscountry
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

def init():
    """"initializing the computations and calling the template"""
    app.ir=inrun4.Inrun()
    app.ir.C=0.05
    app.ir.D=0.4
    app.ir.A=app.ir.D/app.ir.m
    app.ir.inrun()
    app.kode=app.ir.takeoff2()
    app.lent=lento2.Lento(app.ir.sx[app.kode],app.ir.sy[app.kode],app.ir.vx[app.kode],app.ir.vy[app.kode])
    app.lent.D=0.4
    app.lent.A=app.lent.D/app.lent.m
    app.alast=land.Land(takeheight=1,length=10,landangle=30,landheight=10,takesx=app.ir.sx[app.kode],takesy=app.ir.sy[app.kode])
    app.osuma=inter.osuma(app.lent,app.alast)
    #app.form.desitime.data=app.
    print app.lent.t[app.osuma]
    print "osuma-aika"

@app.route("/", methods=['GET','POST'])
def simple():
    app.form = Data(request.form)
    init()
    if request.method == 'POST':
        radius = request.form['radius']
        print radius
        print "tassa on se radius--------------------------------"
        return render_template_string(completed_template, form=app.form)

    else:
        return render_template_string(template_form, form=app.form)

##################################################
## This is the default computation ##
##################################################

@app.route('/plot.png')
def plot(angle=24., ylengthstr=24.,  radius=25.,radius2=20., flat=4,takeoffAngle=20.*2.*numpy.pi/360., takeoffHeight=4.):
    app.fig = Figure()
    app.axis = app.fig.add_subplot(1, 1, 1)



    app.ir.ylengthstr=ylengthstr
    app.ir.runangle=angle*2.*numpy.pi/360.
    app.ir.radius=radius
    app.ir.radius2=radius2
    app.ir.flat=flat
    app.ir.takeoffAngle=takeoffAngle
    app.ir.takeoffHeight=takeoffHeight


    app.ir.inrun()
    app.kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[app.kode]
    syloppu=app.ir.sy[app.kode]
    vxloppu=app.ir.vx[app.kode]
    vyloppu=app.ir.vy[app.kode]

    app.lent.laske(sxloppu,syloppu,vxloppu,vyloppu)
    app.alast.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sxloppu,syloppu)
    app.osuma=inter.osuma(app.lent,app.alast)
    print "Osumakohtiaaaa!!"
    print app.osuma
    app.form.desitime.data=app.lent.t[app.osuma]
    print app.form.desitime.data

# there is time 4.5sec in lento2
# dt is the size of timestep so to reach desiredtime go to step desiredtime/dt
# by default desiredtime =2
    xs = app.lent.sx
    ys = app.lent.sy

    app.axis.plot(xs[:app.osuma], ys[:app.osuma],color="red",linewidth=2,label="flightpath")
    app.axis.plot(app.ir.sx[:app.kode], app.ir.sy[:app.kode], color="black" , linewidth=1, label = "kicker")
    app.axis.plot(app.alast.xx, app.alast.yy, color="black" , linewidth=1, label = "kicker")
#    app.axis.fill_between(app.ir.sx[:app.kode], -40, app.ir.sy[:app.kode], color="black" )

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
    app.lent.A=app.form.airdrag.data
    app.lent.A=app.lent.D/app.lent.m
    app.ir.ylengthstr=app.form.height.data
    app.ir.runangle=app.form.angle.data*2.*numpy.pi/360.
    app.ir.radius=app.form.radius.data
    app.ir.radius2=app.form.radius2.data
    app.ir.flat=app.form.flat.data
    app.ir.takeoffAngle=app.form.takeangle.data*2.*numpy.pi/360.
    app.ir.takeoffHeight=app.form.takeheight.data


    app.ir.inrun()
    app.kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[app.kode]
    syloppu=app.ir.sy[app.kode]
    vxloppu=app.ir.vx[app.kode]
    vyloppu=app.ir.vy[app.kode]

    app.lent.laske(sxloppu,syloppu,vxloppu,vyloppu)
    app.alast.reset(app.form.landdrop.data,app.form.landlength.data,app.form.landangle.data,app.form.landheight.data,sxloppu,syloppu)
    app.osuma=inter.osuma(app.lent,app.alast)

    print "Hang time hang time...!!"
    print app.osuma
    app.form.desitime.data=app.lent.t[app.osuma]

    # there is time 4.5sec in lento2
# dt is the size of timestep so to reach desiredtime go to step desiredtime/dt
# by default desiredtime =2
    xs = app.lent.sx
    ys = app.lent.sy

    app.axis.plot(xs[:app.osuma], ys[:app.osuma],color="red",linewidth=2,label="flightpath")
    app.axis.plot(app.ir.sx[:app.kode], app.ir.sy[:app.kode], color="black" , linewidth=1, label = "kicker")
    app.axis.plot(app.alast.xx, app.alast.yy, color="black" , linewidth=1, label = "kicker")
#    app.axis.fill_between(app.ir.sx[:app.kode], -40, app.ir.sy[:app.kode], color="black" )
    app.axis.legend(loc='upper right')
    app.canvas = FigureCanvas(app.fig)
    app.output = StringIO.StringIO()
    app.canvas.print_png(app.output)
    app.response = make_response(app.output.getvalue())
    app.response.mimetype = 'image/png'
    return app.response


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    app.run(debug=True)

