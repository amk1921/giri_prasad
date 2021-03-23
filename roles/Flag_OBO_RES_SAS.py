# Python module imports
import os
import sys
import datetime
import cx_Oracle  # pip install cx_Oracle  --> to install this library
import logging
import PasswordSAS

# Global variables declaration
wfiles = "/scpa01/projects/SAI_Data_Center/Production/Output/NVO/DCL/Working_Files/"
logs_path = "/home"
now_time = datetime.datetime.now()
today_date = now_time.strftime("%Y-%m-%d_%H%M%S")
logs_path = "/opt/logs/scripts_logs"
log_file = os.path.join(logs_path, sys.argv[0].split('.')[0] + "_" + today_date + ".log")

if not os.path.exists(wfiles):
    print("{0}\nDirectory doesn't exist, exiting from script ..".format(wfiles))
    exit()

def run_sql_query(db_cursor=None, query=None):
    try:
        db_cursor.execute(query)
        logger.info("{0}\nQuery executed successfully".format(query))
    except cx_Oracle.DatabaseError as e:
        logger.exception("{0}\nProblem while executing the above query\n{1}".format(query, e))

def create_db_connection(host=None, user=None, passwd=None):
    try:
        db_connection = cx_Oracle.connect("{0}/{1}@{2}".format(user,passwd, host)
        if db_connection:
            logger.info("Successfully onnected to Oracle Server ....")
            return db_connection
    except cx_Oracle.DatabaseError as e:
        logger.exception("Error while connecting to MySQL DB\n{0}".format(e))

def get_db_cursor(session=None):
    try:
        if session:
            db_cursor = session.cursor()
            return db_cursor
    except cx_Oracle.DatabaseError as e:
        logger.exception("Error while getting cursor for connection {0}\n{1}".format(session, e))

def close_db_connection(session=None, cur=None):
    try:
        if cur:
            cur.close()
            logger.info("DB curose successfully closed\n{0}".format(cur))
        if session:
            session.close()
            logger.info("DB connection successfully closed\n{0}".format(session))
    except cx_Oracle.DatabaseError as e:
        logger.exception("Problem while close DB connection\n{0}".format(e))

def main():
    connection = create_db_connection(host=host_name, db=db_name, user=user_name, passwd=pass_word)
    cursor = get_db_cursor(session=connection)
    drop_table(cursor, "test_table")
    sql_data = fetch_sql_query_data(cursor, "select count(*) from test_table;")
    print(sql_data)
    run_sql_query(cursor, "create table wfiles.OBO_RESERVATIONS as select  RES_ID, OBO_SHIP_SOURCE, OBO_INDICATOR from connection to seaware ( select rp.RES_ID, cast('Y' as CHAR(1)) as OBO_INDICATOR, CASE WHEN PARAM_VALUE IN ('ODM','ODM_DVC','DMOBFF','ODM_SHIP','ODM_REINSTATE') THEN 'DM' WHEN PARAM_VALUE IN ('ODW','ODW_DVC','DWOBFF','ODW_SHIP','ODW_REINSTATE') THEN 'DW' WHEN PARAM_VALUE IN ('ODD','ODD_DVC','DDOBFF','ODD_SHIP','ODD_REINSTATE') THEN 'DD' WHEN PARAM_VALUE IN ('ODF','ODF_DVC','DFOBFF','ODF_SHIP','ODF_REINSTATE') THEN 'DF' END AS OBO_SHIP_SOURCE from seaware.res_param rp where rp.PARAM_CODE = 'REFERRAL_SOURCE' and rp.PARAM_VALUE IN ('ODM','ODM_DVC','DMOBFF','ODM_SHIP','ODM_REINSTATE', 'ODW','ODW_DVC','DWOBFF','ODW_SHIP','ODW_REINSTATE', 'ODD','ODD_DVC','DDOBFF','ODD_SHIP','ODD_REINSTATE', 'ODF','ODF_DVC','DFOBFF','ODF_SHIP','ODF_REINSTATE'))")
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