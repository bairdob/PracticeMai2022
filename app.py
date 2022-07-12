from flask import Flask
from flask import redirect, render_template, url_for, request

from wtforms.form import Form
from wtforms.fields import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp

from shapely import wkt
from shapely.geometry import Point, LineString

from pyproj import Geod

import requests
import rasterio

app = Flask(__name__)

PATTERN_POINT = '^POINT\([-]?[0-9]*.[0-9]+ [-]?[0-9]*.[0-9]+\)'

class DataForm(Form):
    input_point1 = StringField(
        label='point1',
        default='POINT(0.0 0.0)',
        description = 'Начальная точка в формате WKT',
        validators=[DataRequired(), Regexp(PATTERN_POINT)])
    input_point2 = StringField(
        label='point2',
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
    return redirect(url_for('elevation'))


@app.route('/orthodromy', methods=['GET', 'POST'])
def orthodromy():
    orthodromyForm = DataForm(request.form)

    linestring_url= url_for('calculate_orthodrome_line',
                         point1=orthodromyForm.input_point1.data,
                         point2=orthodromyForm.input_point2.data,
                         cs=orthodromyForm.input_coordinate_system.data,
                         count=orthodromyForm.input_count.data, 
                         _external =True)

    return render_template('orthodromy.html',
                           orthodromyForm=orthodromyForm,
                           exampleurl=linestring_url)


def getPolylineWkt(point1, point2, n):
    geoid = Geod(ellps="WGS84")
    interpolated_points = geoid.npts(point1.x, point1.y, point2.x, point2.y, n)

    points = str(point1.x) + ' ' + str(point1.y) + ', ' #add point1 
    points += str(interpolated_points).strip('[]').replace(',', '').replace(
        '(', '').replace(')', ',')
    points += ' ' + str(point2.x) + ' ' + str(point2.y)  #add point2 

    linestring = 'LINESTRING(' + points + ')'

    return linestring


@app.route('/api/calculate_orthodrome_line', methods=['GET'])
def calculate_orthodrome_line():
    point1 = wkt.loads(request.args.get('point1'))  # return Point(x,y)
    point2 = wkt.loads(request.args.get('point2'))
    cs = request.args.get('cs')
    count = int(request.args.get('count'))

    if cs == 'СК-42':
        linestring = getPolylineWkt(point1, point2, count)
        return linestring, 200

    return 'Wrong coordinate system', 400


@app.route('/elevation', methods=['GET', 'POST'])
def elevation():
    
    return render_template('elevation.html')


ELEVATION_FILE = 'static/srtm_N55E160.tif'

def get_elevation(lat, lon, file):
    coords = ((lat, lon), (lat, lon))
    with rasterio.open(file) as src:
        vals = src.sample(coords)
        for val in vals:
            elevation=val[0]
            return elevation

def get_list_coords_3d(iterable_object):
    '''
    return list of (lat,lon,elevation) objects
    '''
    list_coords_3d = []
    for coord in iterable_object:
        elevation =  get_elevation(coord[0], coord[1], ELEVATION_FILE)
        coord_3d = (coord[0], coord[1], elevation) 
        list_coords_3d.append(coord_3d)
    return list_coords_3d

@app.route('/api/elevation', methods=['GET'])
def calculate_elevation():
    wkt_input = request.args.get('wkt')
    wkt_type = wkt_input.split('(')[0]
    
    if (wkt_type == 'POINT'):
        point = wkt.loads(wkt_input) # return Point(x,y)
        elevation = get_elevation(point.x, point.y, ELEVATION_FILE)
        wkt_string = Point([point.x, point.y, elevation]).wkt
        
    elif (wkt_type == 'LINESTRING'):
        wkt_2d = wkt.loads(wkt_input)
        list_coords_3d = get_list_coords_3d(wkt_2d.coords)
        wkt_string = LineString(list_coords_3d).wkt

    elif (wkt_type == 'POLYGON'):
        wkt_string = 'POLYGON'

    return wkt_string, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
