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

from flask import Flask, make_response, render_template, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)
app.angle=25.*2*numpy.pi/360.



@app.route("/")
def simple():
    return render_template('default.html')




@app.route('/plot.png')
def plot(angle=25.):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    runangle=angle*2.*numpy.pi/360.
    ylengthstr=20.
    radius=20.
    app.ir=inrun3.Inrun()
    app.ir.inrun()
    kode=app.ir.takeoff2()

    sxloppu=app.ir.sx[kode]
    syloppu=app.ir.sy[kode]
    vxloppu=app.ir.vx[kode]
    vyloppu=app.ir.vy[kode]

    lent=lento2.Lento(sxloppu,syloppu,vxloppu,vyloppu)
    lent.laske(sxloppu,syloppu,vxloppu,vyloppu)
	
#test for plotting computations
    xs = lent.sx
    ys = lent.sy

    axis.plot(xs, ys)
    axis.plot(app.ir.sx[:kode], app.ir.sy[:kode])
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response




@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/plot/<float:angle>')
def recompute(angle):
    return plot(angle)

if __name__ == '__main__':
    app.run(debug=True)
