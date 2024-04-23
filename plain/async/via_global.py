import asyncio
from contextlib import asynccontextmanager

import aiomysql
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from fastapi import FastAPI

from model import Record

import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    loop = asyncio.get_event_loop()
    pool = await aiomysql.create_pool(host=config.host, port=3306,
                                      user=config.user, password=config.password,
                                      db=config.database, loop=loop)
    async with pool.acquire() as conn, conn.cursor() as cursor:
        await cursor.execute(f"truncate {config.database}.user_event")
        await conn.commit()
    yield
    pool.close()
    await pool.wait_closed()


app = FastAPI(lifespan=lifespan)


@app.post("/add")
async def add_record(data: Record):
    global pool
    async with pool.acquire() as conn, conn.cursor() as cursor:
        await cursor.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        await conn.commit()
    return {"status": 200}
