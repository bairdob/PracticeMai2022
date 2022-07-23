from flask import Flask
from flask import redirect, render_template, url_for, request

from wtforms.form import Form
from wtforms.fields import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp

from shapely import wkt
from shapely.geometry import Point, LineString, Polygon

from pyproj import Geod

import requests
import rasterio
import re

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

    return render_template('orthodromy.html', orthodromyForm=orthodromyForm)


def getPolylineWkt(point1, point2, n):
    '''
    Gets interpolating orthodrome between two (lon,lat) points and 
    formats to Well-known text (WKT) 
                
    reference link: https://gis.stackexchange.com/questions/311362/interpolating-orthodrome-between-two-lon-lat-points-in-python

    Parameters:
        point1 (Point(x,y)): from shapely.geometry
        point2 (Point(x,y)): from shapely.geometry
        n (int): enterpolating points

    Returns:
        str: Returning WKT
    '''

    geoid = Geod(ellps="WGS84")
    interpolated_points = geoid.npts(point1.x, point1.y, point2.x, point2.y, n)

    interpolated_points.insert(0, (point1.x, point1.y)) # add point1
    interpolated_points.append((point1.x, point1.y)) # add point2
    points = ', '.join(map(lambda x: str(x[0]) + ' ' + str(x[1]), interpolated_points))

    return ''.join(['LINESTRING(', points, ')']) 


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
    '''
    Getting elevation at particular coordinate (lat/lon)

    reference link: https://gis.stackexchange.com/questions/228920/getting-elevation-at-particular-coordinate-lat-lon-programmatically-but-offli 

    Parameters:
        lat (int): Point latitude
        lon (int): Point longitude 
        file (str): patth go GeoTIFF file

    Returns:
        int: Returning elevation value at the point 
    '''

    coords = ((lat, lon), (lat, lon))
    with rasterio.open(file) as src:
        vals = src.sample(coords)
        for val in vals:
            elevation=val[0]
            return elevation

def get_list_coords_3d(iterable_object):
    '''
    Return list of (lat,lon,elevation) objects

    Parameters:
        iterable_object (list)

    Returns:
        list: list of (lat,lon,elevation) objects
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
        # parse input to [(lan,lon), (lat,lon), ...]
        points = wkt_input[wkt_input.find("(")+2:wkt_input.find(")")]
        digits = re.findall("\d+\.\d+", points)
        digits_f = [float(it) for it in digits]
        group_points = [digits_f[i:i+2] for i in range(0, len(digits_f), 2)]
        
        list_coords_3d = get_list_coords_3d(group_points)
        wkt_string =Polygon(list_coords_3d).wkt

    return wkt_string, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
