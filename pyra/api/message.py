from http.server import BaseHTTPRequestHandler
import urllib.parse

from src.db import *

'''
class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        db = get_database()
        query = urllib.parse.urlparse(self.path).query
        qs = urllib.parse.parse_qs(query)

        try:
            val = qs['usr'][0]
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
'''

db = get_database()

def upsert(db, cust_id, season_year, season_quarter, race_week_num, message, track_id, series_id):
    upsert_message(db, cust_id, season_year, season_quarter, race_week_num, message, track_id, series_id)

def get(db, cust_id, season_year, season_quarter, race_week_num, series_id):
    result = get_messages(db, cust_id, season_year, season_quarter, race_week_num, series_id)
    return result

upsert(db, 182407, 2022, 1, 1, 'test message 3', 1, 1)
#upsert(db, 182407, 2022, 1, 1, 'test message 2', 1, 1)

result = get(db, 182407, 2022, 1, 1, 1)
print(result)

close_database(db)