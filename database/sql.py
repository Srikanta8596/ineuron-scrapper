import mysql.connector
import logging
from database.configuration import SQL_DATABASE_NAME, SQL_HOST, SQL_AUTH_PLUGIN, SQL_PASSWORD, SQL_TABLE_NAME, SQL_USER_NAME,AUTO_COMMIT

class sqlOperation:
    def __init__(self):
        self.host=SQL_HOST
        self.user=SQL_USER_NAME
        self.password=SQL_PASSWORD
        self.auth_plugin= SQL_AUTH_PLUGIN
        self.db_name=SQL_DATABASE_NAME
        self.table_name=SQL_TABLE_NAME
        self.auto_commit=AUTO_COMMIT
    
    def connect_db(self):
        con=mysql.connector.connect(    
            host=self.host,
            user=self.user,
            password = self.password,
            auth_plugin= self.auth_plugin,
            autocommit=self.auto_commit
            )
        return con


    def creat_db(self,con):
        if (con.is_connected()):
            cur=con.cursor()
            logging.info( "Database is connected")
            #if database not avaialbe create database
            try:
                db_creation_command= f'create database {self.db_name}'
                cur.execute(db_creation_command)
            except Exception as e:
                logging.info(e)
                logging.info("Database exist")
        else:
            logging.info( "Mysql is not connected")

    def create_table(self,con):
        
        if (con.is_connected()):
            cur=con.cursor()
            use_database_command=f'use {self.db_name}'
            cur.execute(use_database_command)
            try:
                create_table_command= f'create table {self.table_name} (course_name  varchar(1000),  course_description varchar(5000))'
                cur.execute(create_table_command)
            except Exception as e:
                logging.info(e)
                logging.info("Table exist")
        else:
            logging.info( "Mysql is not connected")


    
    def insert(self,con, course_name, course_description):
        if (con.is_connected()):
            cur=con.cursor()
            use_database_command=f'use {self.db_name}'
            cur.execute(use_database_command)
            try:
                insert_command= f'insert into {self.table_name} values ( "{course_name}", "{course_description}")'
                cur.execute(insert_command)
            except Exception as e:
                logging.info("Unable insert the element: ",e)
        else:
            logging.info( "Mysql is not connected")