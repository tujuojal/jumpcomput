#!/usr/bin/env python

import StringIO
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, make_response, render_template, render_template_string, request
from wtforms import Form, SelectMultipleField, DecimalField

application = app = Flask(__name__)  #Flask('wsgi')

class LanguageForm(Form):
    language = SelectMultipleField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

class Data(Form):
    radius = DecimalField('Radius of tranny',default=20)
    angle = DecimalField('Angle of inrun',default=24)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Data(request.form)

    if request.method == 'POST':
        print "POST request and form is valid"
        radius = request.form['radius']
        print "radius in blahvala:" 
        return render_template('valmis.html', form=form)

    else:

        return render_template('pohja.html', form=form)

@app.route('/plot.png')
def kuva():
    app.fig = Figure()
    app.axis = app.fig.add_subplot(1, 1, 1)
    app.axis.plot(random.random(),random.random(),color="red")
    app.axis.legend(loc='upper right')
    app.canvas = FigureCanvas(app.fig)
    app.output = StringIO.StringIO()
    app.canvas.print_png(app.output)
    app.response = make_response(app.output.getvalue())
    app.response.mimetype = 'image/png'
    return app.response
if __name__ == '__main__':
    app.run(debug=True)


