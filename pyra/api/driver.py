from http.server import BaseHTTPRequestHandler
import urllib.parse

from src.db import *

class handler(BaseHTTPRequestHandler):

    def get_driver_by_id(db, id, maxItems):
        print('get_driver_by_id')
        result = get_drivers(db, { 'custid': id }, True, maxItems)
        return result

    def get_drivers_by_name(db, name, maxItems):
        print('get_drivers_by_name')
        result = get_drivers(db, { 'displayname': name }, False, maxItems)
        return result

    def do_GET(self):
        MAX_ITEMS = 5

        db = get_database()
        query = urllib.parse.urlparse(self.path).query
        qs = urllib.parse.parse_qs(query)

        try:
            val = qs['usr'][0]
            print(val)
            if isinstance(val, int):
                output = self.get_driver_by_id(db, val, MAX_ITEMS)
            elif isinstance(val, str):
                output = self.get_drivers_by_name(db, val, MAX_ITEMS)
        except:
            print('Missing parameters')
            return
        
        close_database(db)

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))
        return