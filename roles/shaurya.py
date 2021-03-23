# Python module imports
import os
import sys
import datetime
import mysql.connector
from mysql.connector import Error
import logging

# Global variables declaration
host_name = "localhost"
db_name = "db"
user_name = "user"
pass_word = "password"
logs_path = "/home"
now_time = datetime.datetime.now()
today_date = now_time.strftime("%Y-%m-%d_%H%M%S")
logs_path = "/opt/logs/scripts_logs"
log_file = os.path.join(logs_path, sys.argv[0].split('.')[0] + "_" + today_date + ".log")

def drop_table(db_cursor=None, table=None):
    try:
        drop_table_query="DROP database {0} if exists;".format(table)
        db_cursor.execute(drop_table_query)
        logger.info("Table dropped successfully --> {0}".format(table))
    except Exception as e:
        logger.exception("Problem while dropping table --> {0}".format(table))

def run_sql_query(db_cursor=None, query=None):
    try:
        db_cursor.execute(query)
        logger.info("{0}\nQuery executed successfully".format(query))
    except Exception as e:
        logger.exception("{0}\nProblem while executing the above query".format(query))

def fetch_sql_query_data(db_cursor=None, query=None):
    try:
        db_cursor.execute(query)
        query_data = db_cursor.fetchall()
        logger.info("{0}\nQuery executed successfully".format(query))
        return query_data
    except Exception as e:
        logger.exception("{0}\nProblem while fetching data using above query".format(query))

def create_db_connection(host=None, db=None, user=None, passwd=None):
    try:
        db_connection = mysql.connector.connect(host=host,
                                database=db,
                                user=user,
                                password=passwd)
        if db_connection.is_connected():
            db_Info = db_connection.get_server_info()
            logger.info("Successfully onnected to MySQL Server version\n{0} --> {1}".format(db_Info, db))
            return db_connection
    except Error as e:
        logger.exception("Error while connecting to MySQL DB --> {0}".format(db))

def get_db_cursor(session=None):
    try:
        if session.is_connected():
            db_cursor = session.cursor()
            return db_cursor
    except Exception as e:
        logger.exception("Error while getting cursor for connection {0}".format(session))

def close_db_connection(session=None, cur=None):
    try:
        if session.is_connected():
            cur.close()
            session.close()
            logger.info("DB connection successfully closed\n{0}".format(session))
    except Exception as e:
        logger.exception("Problem while close DB connection\n{0}".format(session))

def main():
    connection = create_db_connection(host=host_name, db=db_name, user=user_name, passwd=pass_word)
    cursor = get_db_cursor(session=connection)
    drop_table(cursor, "test_table")
    sql_data = fetch_sql_query_data(cursor, "select count(*) from test_table;")
    print(sql_data)
    run_sql_query(cursor, "create table DL_SALESPLAN_DB.DDE_dedupe_archive as (select dde.*,arch.DATA_AS_OF as PREV_DATA_AS_OF ,////////////////////arch.MILITARY_IND as PREV_MILITARY_IND from PD_SAI_DB.DCL_Extract dde left join DL_SALESPLAN_DB.DCL_Data_Export_archive arch on dde.res_id=arch.res_id) WITH DATA PRIMARY INDEX(RES_ID)) by tera;")
    close_db_connection(session=connection, cur=cursor)


if __name__ == "__main__":
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_file)
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Call main function
    main()