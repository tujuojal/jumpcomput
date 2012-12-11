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
import inrun3

from flask import Flask, make_response, render_template_string, url_for, request
from wtforms import Form, SelectMultipleField, DecimalField
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

############################################################
## Data of the computation via WTForm ##
############################################################

class Data(Form):
    radius = DecimalField('Radius of tranny',default=20)
    angle = DecimalField('Angle of inrun',default=24)
    flat = DecimalField('Length of inrun-flat',default=5)
    height = DecimalField('Height of Inrun',default=24)
    takeheight = DecimalField('Height of Takeoff',default=4)

###########################################################
## Templates for the html as filled and so ##
###########################################################

template_form = """
<title>Computatio</title>
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
<div class=page>
  <h1>Computatio</h1>
    <div class=img>
        <img src="{{ url_for('plot') }}" height="100%" width="100%" alt="Big Boat"> 
    </div>
    
    <button type="button" onclick="alert('This will be a computation \n for simulating jumps')">Click Me!</button>
  {% for message in get_flashed_messages() %}
    <div class=flash>{{ message }}</div>
  {% endfor %}
  {% block body %}{% endblock %}
</div>
{% block content %}
<h1>Set the parameters</h1>

<form method="POST" action="/">
    <div>{{ form.radius.label }} {{ form.radius() }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }}</div>
    <div>{{ form.flat.label }} {{ form.flat() }} {{ form.flat.data }}</div>
    <div>{{ form.height.label }} {{ form.height() }} {{ form.height.data }}</div>
    <div>{{ form.takeheight.label }} {{ form.takeheight() }} {{ form.takeheight.data }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>
{% endblock %}
"""

#########################################################
## and the other template... ##
#########################################################

completed_template = """
<title>Computatio</title>
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
<div class=page>
  <h1>Computatio</h1>
    <div class=img>
        <img src="{{ url_for('replot') }}" height="100%" width="100%" alt="Big Boat"> 
    </div>
    
    <button type="button" onclick="alert('This will be a computation \n for simulating jumps')">Click Me!</button>
  {% for message in get_flashed_messages() %}
    <div class=flash>{{ message }}</div>
  {% endfor %}
  {% block body %}{% endblock %}
</div>
{% block content %}
<h1>Radius Selected</h1>
<form method="POST" action="/">
    <div>{{ form.radius.label }} {{ form.radius() }} {{ form.radius.data }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }} {{ form.angle.data }}</div>
    <div>{{ form.flat.label }} {{ form.flat() }} {{ form.flat.data }}</div>
    <div>{{ form.height.label }} {{ form.height() }} {{ form.height.data }}</div>
    <div>{{ form.takeheight.label }} {{ form.takeheight() }} {{ form.takeheight.data }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>


{% endblock %}

"""
app = Flask(__name__)

def init():
    """"initializing the computations and calling the template"""
    app.ir=inrun3.Inrun()
    app.ir.inrun()
    app.kode=app.ir.takeoff2()
    app.lent=lento2.Lento(app.ir.sx[app.kode],app.ir.sy[app.kode],app.ir.vx[app.kode],app.ir.vy[app.kode])

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
def plot(angle=25., ylengthstr=20., radius=20., flat=5,takeoffAngle=20.*2.*numpy.pi/360., takeoffHeight=4.):
    app.fig = Figure()
    app.axis = app.fig.add_subplot(1, 1, 1)
    
    

    app.ir.ylengthstr=ylengthstr
    app.ir.runangle=angle*2.*numpy.pi/360.
    app.ir.radius=radius
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
	
    xs = app.lent.sx
    ys = app.lent.sy

    app.axis.plot(xs, ys)
    app.axis.plot(app.ir.sx[:app.kode], app.ir.sy[:app.kode])
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

    app.ir.ylengthstr=app.form.height.data
    app.ir.runangle=angle*2.*numpy.pi/360.
    app.ir.radius=app.form.radius.data
    app.ir.flat=flat
    app.ir.takeoffAngle=takeoffAngle
    app.ir.takeoffHeight=app.form.takeheight.data


    app.ir.inrun()
    app.kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[app.kode]
    syloppu=app.ir.sy[app.kode]
    vxloppu=app.ir.vx[app.kode]
    vyloppu=app.ir.vy[app.kode]

    app.lent.laske(sxloppu,syloppu,vxloppu,vyloppu)
	
    xs = app.lent.sx
    ys = app.lent.sy

    app.axis.plot(xs, ys)
    app.axis.plot(app.ir.sx[:app.kode], app.ir.sy[:app.kode])
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
