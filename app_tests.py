import app
import unittest

from app import getPolylineWkt, get_elevation, get_list_coords_3d

from shapely.geometry import Point, LineString, Polygon
from shapely import wkt


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_orthodromy_page(self):
        rv = self.app.get('/orthodromy')
        assert b'/geoapi/calculate_orthodrome_line? point1=' in rv.data

    def test_elevation_page(self):
        rv = self.app.get('/elevation')
        assert b'/api/elevation?' in rv.data

    def index_page(self):
        return self.app.get('/', follow_redirects=True)

    def test_index_redirect(self):
        rv = self.index_page()
        assert b'leaflet.css' in rv.data

    def test_calculate_orthodrome_line_request(self):
        correct = self.app.get("/api/calculate_orthodrome_line?point1=POINT\
                (0.0 0.0)&point2=POINT(0.0 0.0)&cs=СК-42&count=10")
        incorrect = self.app.get("/api/calculate_orthodrome_line?point1=POINT\
                (0.0 0.0)&point2=POINT(0.0 0.0)&cs=СК-43&count=10")

        assert b'LINESTRING' in correct.data
        assert b'Wrong coordinate system' in incorrect.data

    def test_calculate_elevation_request(self):
        point = self.app.get("/api/elevation?wkt=POINT(160.5 55.5)")
        linestring = self.app.get("/api/elevation?wkt=LINESTRING(160.1 55.1, 160.2 55.8)")
        polygon = self.app.get("/api/elevation?wkt=POLYGON((160.34271240234378\
                55.825973254619015, 160.61187744140628 55.87839235515579,\
                160.55145263671878 55.754940702479175,\
                160.72174072265628 55.804368363403064))")

        assert b'POINT Z' in point.data
        assert b'LINESTRING Z' in linestring.data
        assert b'POLYGON Z' in polygon.data


class AdditionalFunctionsTest(unittest.TestCase):

    def test_getPolylineWkt_strReturned(self):
        point1 = Point(0.0, 0.0)     
        point2 = Point(0.0, 0.0)     
        wkt = getPolylineWkt(point1, point2, 10)
        
        assert 'LINESTRING' in wkt 

    def test_get_elevatation_intReturned(self):
        lat1, lon1 = 0.0, 0.0
        lat2, lon2 = 160.5, 55.5
        geotif = 'static/srtm_N55E160.tif'

        elevation_no_data = get_elevation(lat1, lon1, geotif)
        elevation = get_elevation(lat2, lon2, geotif)

        self.assertEqual(-32768, elevation_no_data)
        self.assertEqual(639 , elevation)

    def test_get_list_coords_3d_listReturned(self):
        linestring = 'LINESTRING(160.1 55.1, 160.2 55.8)'
        linestring_2d = wkt.loads(linestring)
        list_3d = get_list_coords_3d(linestring_2d.coords)
        
        self.assertIsInstance(list_3d, list)
        self.assertEqual(len(list_3d), 2)

 
if __name__ == '__main__':
    unittest.main()
