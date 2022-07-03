from flask import Flask
from flask import redirect, render_template, url_for, request

from wtforms.form import Form
from wtforms.fields import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp

from shapely import wkt
from pyproj import Geod

import re
import requests

app = Flask(__name__)

PATTERN_POINT = '^POINT\([0-9]*.[0-9]+ [0-9]*.[0-9]+\)'


class DataForm(Form):
    input_point1 = StringField(
        default='POINT(0.0 0.0)',
        validators=[DataRequired(), Regexp(PATTERN_POINT)])
    input_point2 = StringField(
        default='POINT(0.0 0.0)',
        validators=[DataRequired(), Regexp(PATTERN_POINT)])
    input_coordinate_system = SelectField(choices=[('СК-42'), ('другое')])
    input_count = StringField(default='10',
                              validators=[DataRequired(),
                                          Regexp('^[0-9]+$')])
    output_linestring = TextAreaField('LINESTRING(0.0)')
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return redirect(url_for('orthodromy'))


@app.route('/orthodromy', methods=['GET', 'POST'])
def orthodromy():
    orthodromyForm = DataForm(request.form)
    orthodromyForm.input_point1.label = 'point1'
    orthodromyForm.input_point1.description = 'Начальная точка в формате WKT'
    orthodromyForm.input_point2.label = 'point2'
    orthodromyForm.input_point2.description = 'Конечная точка в формате WKT'
    orthodromyForm.input_coordinate_system.label = 'cs'
    orthodromyForm.input_coordinate_system.description = 'Система координат'
    orthodromyForm.input_count.label = 'count'
    orthodromyForm.input_count.description = 'Количество рассчитываемых точек, по-умолчанию 10'

    if request.method == 'POST' and orthodromyForm.validate():
        linestring = url_for('calculate_orthodrome_line',
                             point1=orthodromyForm.input_point1.data,
                             point2=orthodromyForm.input_point2.data,
                             cs=orthodromyForm.input_coordinate_system.data,
                             count=orthodromyForm.input_count.data)
        my_url = "http://127.0.0.1:5000" + linestring

        orthodromyForm.output_linestring.data = requests.post(url=my_url).text

        return render_template('orthodromy.html', orthodromyForm=orthodromyForm)

    return render_template('orthodromy.html', orthodromyForm=orthodromyForm)


@app.route('/api/calculate_orthodrome_line', methods=['GET', 'POST'])
def calculate_orthodrome_line():
    point1 = wkt.loads(request.args.get('point1'))  # return Point(x,y)
    point2 = wkt.loads(request.args.get('point2'))
    cs = request.args.get('cs')
    count = int(request.args.get('count'))

    if cs == 'СК-42':
        geoid = Geod(ellps="WGS84")
        extra_points = geoid.npts(point1.x, point1.y, point2.x, point2.y,
                                  count)

        points = str(extra_points).strip('[]').replace(',', '').replace(
            '(', '').replace(')', ',')
        linestring = 'LINESTRING(' + points.strip(',') + ')'

        return linestring, 200

    return 'Wrong coordinate system', 400


if __name__ == '__main__':
    app.run(debug=True)
