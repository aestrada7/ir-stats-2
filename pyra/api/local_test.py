from src.auth import *
from src.db import *
from src.constants import *
from src.iracing_api import *

db = get_database()
[sess, cust_id] = authenticate(db, 'usr', 'pwd')

if cust_id != 0:
    get_results(db, sess, cust_id, Constants.SERIES_ID_INDY_FIXED_OVAL, 2024, 2, 1)
else:
    print('Authentication failed')

close_database(db)