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
            val = qs['cust_id'][0]
            print(val)

            output = get_seasons(db, Constants.SERIES_ID_INDY_FIXED_OVAL, val)

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