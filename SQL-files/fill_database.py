import mysql.connector
import datetime as dt
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

host = "localhost"
user = "root"
password = "1212"

def connection(database: str) -> PooledMySQLConnection | MySQLConnectionAbstract:
    return mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )


def add_users(database: str, count: int):
    with connection(database) as conn, conn.cursor() as cursor:
        sql = """
        replace into users (name, surname, username, email, region, birthdate) VALUES
        """
        for i in range(count):
            sql += f"('name{i+1}', 'surname{i+1}', 'user{i+1}', 'email{i+1}', 0, '{dt.datetime.now()}'),\n"
        cursor.execute(sql[:-2])
        conn.commit()


def add_events(database: str, count: int, author_id: int, partly = False):
    if not partly:
        with connection(database) as conn, conn.cursor() as cursor:
            sql = """
            replace into events (title, address, region, description, price, max_people, category, is_online, start_date, end_date, icon, author, creation_date) VALUES
            """
            for i in range(count):
                sql += f"('event{i+1}', 'some address', 0, '', 0, 1, 0, 0, '{dt.datetime.now().date()}', '{dt.datetime.now().date()}', 0, {author_id}, '{dt.datetime.now().date()}'),\n"
            cursor.execute(sql[:-2])
            conn.commit()
    else:
        for start in range(0, count, count // 1000):
            with connection(database) as conn, conn.cursor() as cursor:
                sql = """
                replace into events (id, title, address, region, description, price, max_people, category, is_online, start_date, end_date, icon, author, creation_date) VALUES
                """
                for i in range(start, start + count // 1000 + 1):
                    sql += f"({i}, 'event{i + 1}', 'some address', 0, '', 0, 1, 0, 0, '{dt.datetime.now().date()}', '{dt.datetime.now().date()}', 0, {author_id}, '{dt.datetime.now().date()}'),\n"
                cursor.execute(sql[:-2])
                conn.commit()


if __name__ == "__main__":
    add_users("science_small", 10)
    add_users("science_big", 100000)
    add_events("science_small", 50, 55),
    add_events("science_big", 1_000_000, 55, True)
