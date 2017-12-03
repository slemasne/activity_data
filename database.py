import datetime
import pandas as pd
import sqlite3

static = 'C:\\Users\\Stephen\\Desktop\\sp\\flask\\tyred\\static\\'


def datetime_now():
    return "This web page was generated at: " + datetime.datetime.now().strftime("%H:%M:%S")

def datetime_today():
    return datetime.datetime.now().strftime("%d/%m/%y")

def drop_db():
    with sqlite3.connect("workouts.db") as db:
        c = db.cursor()
        c.execute("DROP TABLE workouts")
    db.close()

def create_db():
    with sqlite3.connect("workouts.db") as db:
        c = db.cursor()
        c.execute("CREATE TABLE workouts(workout_id NUMBER, workout_date TEXT, workout_type TEXT, visits TEXT, distance NUMBER, entry_date TEXT, entry_time TEXT);")
        db.commit()
    db.close()

def update_db(workout_id, workout_date, workout_type, visits, distance, entry_date, entry_time):
    with sqlite3.connect("workouts.db") as db:
        c = db.cursor()
        c.execute("INSERT INTO workouts VALUES(?,?,?,?,?,?,?);", (workout_id, workout_date, workout_type, visits, distance, entry_date, entry_time))
        db.commit()
    db.close()

def view_dbold():
    with sqlite3.connect("workouts.db") as db:
        c = db.cursor()
        for row in c.execute('SELECT * FROM workouts'):
            print row
    db.close()

def view_db():
    cnx = sqlite3.connect('workouts.db')
    df = pd.read_sql_query("SELECT * FROM workouts", cnx)
    return df

def view_workout_legacy():
    cnx = sqlite3.connect('workout_legacy.db')
    df = pd.read_sql_query("SELECT * FROM workouts", cnx)
    return df

#drop_db()
#create_db()
#update_db("cycle","London")
#print view_workout_legacy()

#path = r"C:\Users\Stephen\Desktop\sp\flask\tyred\static\csv\workout_results.csv"
#csv = view_db().to_csv(path, encoding='utf-8')

print static