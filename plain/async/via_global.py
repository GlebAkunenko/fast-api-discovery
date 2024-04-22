import asyncio
from contextlib import asynccontextmanager

import aiomysql
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from fastapi import FastAPI

from model import Record

import config

app = FastAPI(prefix="/plain/sync")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    loop = asyncio.get_event_loop()
    pool = await aiomysql.create_pool(host=config.host, port=3306,
                                                user=config.user, password=config.password,
                                                db=config.database, loop=loop)
    yield
    pool.close()
    await pool.wait_closed()


@app.post("/add")
def add_record(data: Record):
    global pool
    with pool.acquire() as conn, conn.cursor() as cursor:
        cursor.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        conn.commit()
    return {"status": 200}

