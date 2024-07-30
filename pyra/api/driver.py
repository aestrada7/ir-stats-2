from http.server import BaseHTTPRequestHandler
import urllib.parse
import json

from src.db import *

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        MAX_ITEMS = 5

        db = get_database()
        query = urllib.parse.urlparse(self.path).query
        qs = urllib.parse.parse_qs(query)
        output = ""

        try:
            val = qs['usr'][0]
            try:
                val = int(val)
            except ValueError:
                val = str(val)
            print(val)

            if isinstance(val, int):
                output = get_drivers(db, { 'custid': val }, True, MAX_ITEMS)
            elif isinstance(val, str):
                output = get_drivers(db, { 'displayname': val }, False, MAX_ITEMS)

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