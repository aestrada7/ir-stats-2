from fastapi.responses import StreamingResponse
from fastapi import APIRouter
import asyncio
import time
import multiprocessing
from src.db import *

router = APIRouter()
q = multiprocessing.Manager().Queue()

def write_to_database(q):
    for i in range(10):
        q.put(f"Writing to queue {i}")
        time.sleep(1)

@router.get("/test")
async def test_route():
    data = [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        {"id": 3, "name": "Taylor"},
        {"id": 4, "name": "Michael"},
        {"id": 5, "name": "William"},
        {"id": 6, "name": "David"},
        {"id": 7, "name": "Richard"},
        {"id": 8, "name": "Joseph"},
        {"id": 9, "name": "Thomas"},
        {"id": 10, "name": "Charles"}
    ]

    #p = multiprocessing.Process(target=write_to_database, args=(q,))
    p = multiprocessing.Process(target=process_test, args=(q, data,))
    p.start()
    async def chunks():
        while p.is_alive() or not q.empty():
            if not q.empty():
                data = q.get()
                yield f"data: {data}\n"
            else:
                await asyncio.sleep(1)
        yield "done\n"

    return StreamingResponse(chunks(), media_type="text/event-stream")

'''
# easiest way - this works
async def chunks():
    for i in range(4):
        yield "x-data: {}\n\n".format(i)
        await asyncio.sleep(1)

@router.get("/test")
async def test_route():
    return StreamingResponse(chunks(), media_type="text/event-stream")
'''