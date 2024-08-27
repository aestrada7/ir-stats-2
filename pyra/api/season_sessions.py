from http.server import BaseHTTPRequestHandler
import urllib.parse
import json

from src.db import *
from src.constants import *

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        db = get_database()
        query = urllib.parse.urlparse(self.path).query
        qs = urllib.parse.parse_qs(query)
        output = ""

        try:
            cust_id = qs['cust_id'][0]
            series_id = qs['series_id'][0]
            season_year = qs['season_year'][0]
            season_quarter = qs['season_quarter'][0]

            output = get_seasons(db, series_id, cust_id)
            output = get_season_subsessions(db, cust_id, season_year, season_quarter, series_id)

            output = json.dumps(output)
            print(output)
        except:
            print('Missing parameters')
            return
        
        close_database(db)

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))
        return