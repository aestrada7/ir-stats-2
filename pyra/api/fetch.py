import json
from fastapi import APIRouter, Request, Response

from src.auth import *
from src.db import *
from src.constants import *
from src.iracing_api import *

router = APIRouter()

@router.get("/fetch")
def fetch_route(request: Request, usr: str, pwd: str, sid: int, sy: int, sq: int):
    if(usr == None or pwd == None or sid == None or sy == None or sq == None):
        output = { "status": 400, "message": "Missing parameters" }

    user = usr
    password = pwd
    series_id = sid
    season_year = sy
    season_quarter = sq

    db = get_database()
    [sess, cust_id] = authenticate(db, user, password)
    print(cust_id)

    if cust_id != 0:
        get_results(db, sess, cust_id, series_id, season_year, season_quarter, 1)
        output = { "status": 200, "message": f"Successfully synchronized data from {season_year} - Season {season_quarter}." }
    else:
        output = { "status": 403, "message": "Authentication Error. Make sure iRacing is online and that your username/password combination is correct." }

    close_database(db)
    output = json.dumps(output)

    return Response(content=output, media_type='text/plain; charset=utf-8')