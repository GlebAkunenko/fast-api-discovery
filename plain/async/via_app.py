from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.requests import Request

from model import Record

import aiomysql, asyncio, config

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    app.state.pool = await aiomysql.create_pool(host=config.host, port=3306,
                                      user=config.user, password=config.password,
                                      db=config.database, loop=loop)
    yield
    app.state.pool.close()
    await app.state.pool.wait_closed()


app = FastAPI(lifespan=lifespan)


@app.post("/add")
async def add_record(request: Request, data: Record):
    pool = request.app.state.pool
    async with pool.acquire() as conn, conn.cursor() as cur:
        await cur.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        await conn.commit()
    return {"status": 200}

