#!/usr/bin/env python

from flask import Flask, render_template_string, request
from wtforms import Form, SelectMultipleField, DecimalField

application = app = Flask(__name__)  #Flask('wsgi')

class LanguageForm(Form):
    language = SelectMultipleField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])

class Data(Form):
    radius = DecimalField('Radius of tranny',default=20)
    angle = DecimalField('Angle of inrun',default=24)

template_form = """
{% block content %}
<h1>Set Language</h1>

<form method="POST" action="/">
    <div>{{ form.radius.label }} {{ form.radius() }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>
{% endblock %}

"""

completed_template = """
{% block content %}
<h1>Radius Selected</h1>
<form method="POST" action="/">
    <div>{{ form.radius.label }} {{ form.radius() }} {{ form.radius.data }}</div>
    <div>{{ form.angle.label }} {{ form.angle() }} {{ form.angle.data }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>


{% endblock %}

"""

@app.route('/', methods=['GET', 'POST'])
def index():
    form = Data(request.form)

    if request.method == 'POST':
        print "POST request and form is valid"
        radius = request.form['radius']
        print "radius in blahvala:" 
        return render_template_string(completed_template, form=form)

    else:

        return render_template_string(template_form, form=form)

if __name__ == '__main__':
    app.run(debug=True)


