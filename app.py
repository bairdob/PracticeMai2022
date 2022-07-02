from flask import Flask
from flask import redirect, render_template, url_for, request

from geomet import wkt

from wtforms.form import Form
from wtforms.fields import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Regexp

import re

import json

app = Flask(__name__)


def get_geojson_from_wkt(wkt_string):
    return wkt.loads(wkt_string)


# ls = 'POINT(37.6245 55.123123)'
# print(get_geojson_from_wkt(ls))

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
        print('done')
        return render_template('orthodromy.html')

    return render_template('orthodromy.html', orthodromyForm=orthodromyForm)


if __name__ == '__main__':
    app.run(debug=True)
