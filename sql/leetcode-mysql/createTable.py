""" @220828 用于执行LC上的数据表创建语句
输入: input.sql 每行一条语句, 没有分号
"""

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase

from easonsi import utils

# 注意修改数据库配置
conn: MySQLConnection = mysql.connector.connect(
    host="10.88.3.55", 
    # host='100.111.213.48',
    user='root', password='root',
    database="test")

def execute(sql: str):
    cursor:CursorBase = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

for sqlline in utils.LoadList("./input.sql"):
    execute(sqlline)
