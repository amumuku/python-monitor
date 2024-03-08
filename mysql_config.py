import mysql.connector
from logger_setup import logger  # 导入日志记录器

from mysql.connector import pooling




dbconfig = {
        'port': '3306',
        'host': '192.168.100.53',
        'user': 'bot',
        'password': 'hello1234',
        'database': 'ht_mes'
}
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)


def connect_to_mysql():
    try:
        conn = pool.get_connection()
        if conn:
            if conn.is_connected():
                return conn
            else:
                logger.error("MySQL connection is not valid.")
                return None
        else:
            logger.error("Failed to get a connection from the pool.")
            return None
    except Exception as e:
        logger.error("Error connecting to MySQL database: %s", str(e))
        return None

def insert_data(conn, table_name, data):
    try:
        cursor = conn.cursor()
        insert_query = f"INSERT IGNORE INTO {table_name} (watch_account,chain_name, main_balance, block_num) \
        VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        logger.info("Data inserted into MySQL database")
    except Exception as e:
        logger.error("Error inserting data into MySQL database:", str(e))
        close_mysql_connection(conn)

def close_mysql_connection(conn):
    try:
        conn.close()
    except Exception as e:
        logger.error("Error closing MySQL connection:", str(e))
