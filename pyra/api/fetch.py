import json
import asyncio
import multiprocessing
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from src.auth import *
from src.db import *
from src.constants import *
from src.iracing_api import *

router = APIRouter()
q = multiprocessing.Manager().Queue()

@router.get("/fetch")
def fetch_route(request: Request, usr: str, pwd: str, sid: int, sy: int, sq: int):
    user = usr
    password = pwd
    series_id = sid
    season_year = sy
    season_quarter = sq

    db = get_database()
    [sess, cust_id] = authenticate(db, user, password)
    print(cust_id)

    if cust_id != 0:
        p = multiprocessing.Process(target=get_results, args=(q, sess, cust_id, series_id, season_year, season_quarter, 1))
        p.start()
        invalid = False
    else:
        invalid = True

    async def chunks():
        if not invalid:
            while p.is_alive() or not q.empty():
                if not q.empty():
                    data = q.get()
                    yield f"{data}\n"
                else:
                    await asyncio.sleep(1)
            yield "Process completed\n"
        else:
            yield "Authentication Error. Make sure iRacing is online and that your username/password combination is correct."

    return StreamingResponse(chunks(), media_type="text/event-stream")