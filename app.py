from flask import Flask
from flask import redirect, render_template, url_for, request

from wtforms.form import Form
from wtforms.fields import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp

from shapely import wkt
from pyproj import Geod

import re
import requests
import socket

app = Flask(__name__)

HOST = '0.0.0.0'
HOSTDOCKER = str(socket.gethostbyname(socket.gethostname()))
PATTERN_POINT = '^POINT\([-]?[0-9]*.[0-9]+ [-]?[0-9]*.[0-9]+\)'
EXAMPLEURL = 'http://127.0.0.1:5000/api/calculate_orthodrome_line?point1=POINT(37.6135769672713991+55.75410998124817752)&point2=POINT(139.74946157054466767+35.68696276437117376)&cs=СК-42&count=20'


class DataForm(Form):
    input_point1 = StringField(
        label='point1',
        default='POINT(0.0 0.0)',
        description = 'Начальная точка в формате WKT',
        validators=[DataRequired(), Regexp(PATTERN_POINT)])
    input_point2 = StringField(
        label='poin2',
        default='POINT(0.0 0.0)',
        description = 'Конечная точка в формате WKT',
        validators=[DataRequired(), Regexp(PATTERN_POINT)])
    input_coordinate_system = SelectField(
        label='cs',
        choices=[('СК-42', 'СК-42'), ('другое', 'другое')],
        default='СК-42',
        description = 'Система координат')
    input_count = StringField(
        label='count',
        default='10',
        description = 'Количество рассчитываемых точек, по-умолчанию 10',
        validators=[DataRequired(), Regexp('^[0-9]+$')])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return redirect(url_for('orthodromy'))


@app.route('/orthodromy', methods=['GET', 'POST'])
def orthodromy():
    orthodromyForm = DataForm(request.form)

    linestring = url_for('calculate_orthodrome_line',
                         point1=orthodromyForm.input_point1.data,
                         point2=orthodromyForm.input_point2.data,
                         cs=orthodromyForm.input_coordinate_system.data,
                         count=orthodromyForm.input_count.data)

    my_url = request.host_url + linestring
    # my_url = 'http://' + HOSTDOCKER + ':5000'+ linestring

    if request.method == 'POST' and orthodromyForm.validate():
        orthodromyForm.output_linestring.data = requests.get(url=my_url).text

        return render_template('orthodromy.html',
                               orthodromyForm=orthodromyForm,
                               exampleurl=my_url)

    return render_template('orthodromy.html',
                           orthodromyForm=orthodromyForm,
                           exampleurl=my_url)


@app.route('/api/calculate_orthodrome_line', methods=['GET'])
def calculate_orthodrome_line():
    point1 = wkt.loads(request.args.get('point1'))  # return Point(x,y)
    point2 = wkt.loads(request.args.get('point2'))
    cs = request.args.get('cs')
    count = int(request.args.get('count'))

    print(type(point1))
    if cs == 'СК-42':
        geoid = Geod(ellps="WGS84")
        extra_points = geoid.npts(point1.x, point1.y, point2.x, point2.y,
                                  count)
        points = str(point1.x) + ' ' + str(point1.y) + ', ' #add point1 
        points += str(extra_points).strip('[]').replace(',', '').replace(
            '(', '').replace(')', ',')
        points += ' ' + str(point2.x) + ' ' + str(point2.y)  #add point2 

        linestring = 'LINESTRING(' + points + ')'

        return linestring, 200

    return 'Wrong coordinate system', 400


if __name__ == '__main__':
    app.run(debug=True, host=HOST)
