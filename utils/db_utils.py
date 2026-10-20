import pymysql

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_db_connection():
    """创建 MySQL 数据库连接"""

    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
        read_timeout=5,
    )

    return connection


def get_product_by_id(product_id):
    """根据商品ID查询数据库中的商品信息"""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT id, name, price, stock
                FROM pms_product
                WHERE id = %s
            """

            cursor.execute(sql, (product_id,))

            product = cursor.fetchone()

            return product

    finally:
        connection.close()

def get_any_product():
    """从数据库中查询一条商品记录"""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT id, name, price, stock
                FROM pms_product
                ORDER BY id
                LIMIT 1
            """

            cursor.execute(sql)

            return cursor.fetchone()

    finally:
        connection.close()