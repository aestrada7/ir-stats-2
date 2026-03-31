import json
from fastapi import APIRouter, Request, Response
from src.db import *

router = APIRouter()

@router.get("/driver")
async def driver_route(request: Request, usr: str):
    MAX_ITEMS = 5

    db = get_database()
    output = ""
    
    try:
        val = usr
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
        output = { 'error': 'Missing parameters' }
    
    close_database(db)

    return Response(content=output, media_type='text/plain; charset=utf-8')