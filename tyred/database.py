import datetime
import pandas as pd
import sqlite3
import os
import csv

class TimeStmpToday():
    
    """
    Returns timestamps used in the application.
    """

    def __init__(self):
        self.now = datetime.datetime.now()

    def webpage_time(self):
        return "This web page was generated at: " + self.now.strftime("%H:%M:%S")

    def today_date(self):
        return self.now.strftime("%d/%m/%y")

    def today_time(self):
        return self.now.strftime("%H:%M:%S")

class DataBase():

    """
    Returns Database and tables used in the application.
    """

    def __init__ (self, database = "workout.db", table = "workouts"):
        self.database = database
        self.table = table

    def create_table(self):
        csv_file = os.getcwd()+ "\static\\" + "workout_data_clean.csv"
        if os.path.isfile(csv_file):
        	self.create_legacy()
        else:
        	con =  sqlite3.connect(self.database)
        	c = con.cursor()
        	c.execute("drop table if exists workouts")
        	c.execute("""CREATE TABLE workouts (workout_id NUMBER, workout_date TEXT, workout_type TEXT, 
        		distance NUMBER, entry_date TEXT, entry_time TEXT);""")
        	con.commit()

    def update_db(self, workout_id, workout_date, workout_type, distance, entry_date, entry_time):
        con =  sqlite3.connect(self.database)
        c = con.cursor()
        c.execute("INSERT INTO workouts VALUES(?,?,?,?,?,?);", (workout_id, workout_date, workout_type, distance, entry_date, entry_time))
        con.commit()

    def load_df(self):
        con = sqlite3.connect('workout.db')
        df = pd.read_sql_query("SELECT * FROM workouts", con)
        return df

    def load_legacy(self):
        con = sqlite3.connect('workout_legacy.db')
        df = pd.read_sql_query("SELECT * FROM workouts", con)
        return df

    def create_legacy(self):
    	csv_file = os.getcwd()+ "\static\\" + "workout_data_clean.csv"
    	con =  sqlite3.connect(self.database)
        c = con.cursor()
        c.execute("drop table if exists workouts")
        c.execute("""CREATE TABLE workouts (workout_id NUMBER, workout_date TEXT, workout_type TEXT, 
        	distance NUMBER, entry_date TEXT, entry_time TEXT);""")
        con.commit()
        with open(csv_file,'rb') as fin:
        	dr = csv.DictReader(fin)
        	to_db = [(i['workout_id'], i['workout_date'],i['workout_type'],i['distance'],
        		i['entry_date'],i['entry_time'],) for i in dr]
        	c.executemany("""INSERT INTO workouts (workout_id, workout_date, workout_type, distance, entry_date, entry_time) 
        		VALUES (?,?,?,?,?,?);""", to_db)
		con.commit()
		con.close()


