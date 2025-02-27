import json

from src.auth import *
from src.db import *
from src.constants import *
from src.iracing_api import *

db = get_database()

#Auth
#[sess, cust_id] = authenticate(db, 'vanhelsing44@gmail.com', 'aydhvi6d')

#if cust_id != 0:
#    get_results(db, sess, cust_id, Constants.SERIES_ID_INDY_FIXED_OVAL, 2024, 3, 1)
#else:
#    print('Authentication failed')

x = get_track_by_id(db, 116)
print(json.dumps(x))

#Driver query
#print( get_drivers(db, { 'displayname': 'Est' }, False, 5) )
#print( get_drivers(db, { 'custid': '182407' }, True, 5) )

#x = get_seasons(db, Constants.SERIES_ID_INDY_FIXED_OVAL, 182407)

#x = get_season_subsessions(db, 182407, 2024, 3, Constants.SERIES_ID_INDY_FIXED_OVAL)
#print(json.dumps(x))

close_database(db)