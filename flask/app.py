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

from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)

@app.route("/")
def simple():
    data_uri = open("/plot.png", "rb").read().encode("base64").replace("\n", "")
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(data_uri)
    print img_tag




@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    runangle=25.*2.*numpy.pi/360.
    ylengthstr=20.
    radius=20.
    ir=inrun3.Inrun()
    ir.inrun()
    kode=ir.takeoff2()

    sxloppu=ir.sx[kode]
    syloppu=ir.sy[kode]
    vxloppu=ir.vx[kode]
    vyloppu=ir.vy[kode]

    lent=lento2.Lento(sxloppu,syloppu,vxloppu,vyloppu)
    lent.laske(sxloppu,syloppu,vxloppu,vyloppu)
	
#test for plotting computations
    xs = lent.sx
    ys = lent.sy

    axis.plot(xs, ys)
    axis.plot(ir.sx[:kode], ir.sy[:kode])
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    app.run(debug=True)
