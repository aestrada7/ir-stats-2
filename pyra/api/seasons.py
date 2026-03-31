import json
from fastapi import APIRouter, Request, Response
from src.db import *

router = APIRouter()

@router.get("/seasons")
async def seasons_route(request: Request, cust_id: int, series_id: int):
    db = get_database()

    try:
        output = get_seasons(db, series_id, cust_id)
    except:
        output = { "status": 400, "message": "Missing parameters" }

    output = json.dumps(output)
    
    close_database(db)

    return Response(content=output, media_type='text/plain; charset=utf-8')