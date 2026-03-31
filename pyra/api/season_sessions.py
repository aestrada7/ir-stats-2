import json
from fastapi import APIRouter, Request, Response
from src.db import *

router = APIRouter()

@router.get("/season_sessions")
async def season_sessions_route(request: Request, cust_id: int, series_id: int, season_year: int, season_quarter: int):
    db = get_database()

    try:
        output = get_season_subsessions(db, cust_id, season_year, season_quarter, series_id)
    except:
        output = { "status": 400, "message": "Missing parameters" }

    output = json.dumps(output)
    
    close_database(db)

    return Response(content=output, media_type='text/plain; charset=utf-8')