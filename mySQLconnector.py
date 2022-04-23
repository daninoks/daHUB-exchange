#!/usr/bin/env python

import mysql.connector
from mysql.connector import errorcode

from token_generator import token_gen

# Should be pulled from DBPROPERTY class  from config.py:
DB_USER = 'nox'
DB_PASS = 'Password12345!'
DB_HOST = '127.0.0.1'
DB_NAME = 'customers'

databaseConfig = {'user': DB_USER,
                  'password': DB_PASS,
                  'host': DB_HOST,
                  'database': DB_NAME,
                  'raise_on_warnings': True}


class UserAuthorised:
    def __init__(self, userID, userToken, userBanned, dbMessage):
        self.userID = userID
        self.userToken = userToken
        self.userBanned = userBanned
        self.dbMessage = dbMessage


def dataBaseCheckConnection(connection):
    try:
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Error while connecting to MySQL", err)


def customersDataBaseCheck():
    # DB_NAME = 'customers'
    TABLES = {}
    TABLES['customers'] = (
        "CREATE TABLE `customers` ("
        "   `user_id` int(4) NOT NULL AUTO_INCREMENT,"
        "   `user_sha32` varchar(32) NOT NULL,"
        "   `user_banned` tinyint(1),"
        "  PRIMARY KEY (`user_id`)"
        ") ENGINE=InnoDB"
    )
    databaseCreateConfig = {'user': DB_USER,
                            'password': DB_PASS,
                            'host': DB_HOST,
                            'raise_on_warnings': True}

    # DataBase connection establish:
    connection = mysql.connector.connect(**databaseCreateConfig)
    cursor = connection.cursor()

    # Examine if DB exists. Create if not:
    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8mb4'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            connection.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Push DB to MySQL:
    for table_name in TABLES:
        table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    connection.close()
    print("MySQL connection is closed")


def pushDB_NewUser(push_userID, push_userSHA32):
    connection = mysql.connector.connect(**databaseConfig)
    dataBaseCheckConnection(connection)
    cursor = connection.cursor()
    add_customers = ("INSERT INTO customers "
                     "(user_id, user_sha32, user_banned) "
                     "VALUES (%(value_id)s, %(value_sha32)s, %(value_banned)s)")
    data_customers = {'value_id': push_userID,
                      'value_sha32': push_userSHA32,
                      'value_banned': '0'}
    cursor.execute(add_customers, data_customers)
    connection.commit()
    cursor.close()
    connection.close()


def pullDB(query_userID):
    customersDataBaseCheck()
    au = UserAuthorised("", "", "", "")

    connection = mysql.connector.connect(**databaseConfig)
    dataBaseCheckConnection(connection)
    cursor = connection.cursor()

    query = ("SELECT user_id, user_sha32, user_banned FROM customers "
             f"WHERE user_id={query_userID} ")

    cursor.execute(query)
    row = cursor.fetchone()
    print(row)
    if row is None:
        sha32_new = token_gen(32)
        pushDB_NewUser(query_userID, sha32_new)
        au.userID = query_userID
        au.userToken = sha32_new
        au.userBanned = "0"
        au.dbMessage = "New user signed in."
    else:
        if(len(row) == 3):
            au.userID = row[0]
            au.userToken = row[1]
            au.userBanned = row[2]
            if(au.userBanned == "1"):
                au.dbMessage = "Seems this User Banned from our network."
            else:
                au.dbMessage = "User successfully logged in network."
    cursor.close()
    connection.close()
    return au
