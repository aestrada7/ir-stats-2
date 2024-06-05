from http.server import BaseHTTPRequestHandler
import urllib.parse

from src.auth import *
from src.db import *
from src.constants import *
from src.iracing_api import *

class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        qs = urllib.parse.parse_qs(query)

        try:
            user = qs['usr'][0]
            password = base64_decode(qs['pwd'][0])
            series_id = qs['sid'][0]
            season_year = qs['sy'][0]
            season_quarter = qs['sq'][0]
            print(qs)
        except:
            print('Missing parameters')
            return

        db = get_database()
        [sess, cust_id] = authenticate(db, user, password)

        if cust_id != 0:
            get_results(db, sess, cust_id, series_id, season_year, season_quarter, 1)
            output = f'Successfully synchronized data from {season_year} - Season {season_quarter}.'
        else:
            output = 'Authentication Error. Make sure iRacing is online and that your username/password combination is correct.'

        close_database(db)

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))
        return