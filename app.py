from flask import Flask, render_template, request, Response, make_response, send_file
from database import update_db, view_db, drop_db, create_db, datetime_now, datetime_today, view_workout_legacy
import datetime

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/db_reset',methods = ["POST","GET"])
def db_reset():
	drop_db()
	create_db()
	return render_template('db_reset.html')

@app.route('/sample',methods = ["POST","GET"])
def sample():
	df = view_workout_legacy()
	return render_template('legacy_results.html',  table = df.to_html(classes="table-striped"), 
		datetime_today = datetime_today(), datetime_now = datetime_now())

@app.route("/to_csv", methods = ["POST","GET"])
def getWorkoutCSV():
	path = r"C:\Users\Stephen\Desktop\sp\flask\tyred\static\csv\workout_results.csv"
	csv = view_db().to_csv(path, encoding='utf-8')
	return send_file(path, as_attachment=True)

@app.route('/result', methods = ["POST","GET"])
def result():
	request.method == "POST"
	if not request.form['workout_date']:
		workout_date = datetime.datetime.now().strftime("%d/%m/%y")
	else:
		workout_date = request.form['workout_date']
	workout_id = "TestID_1001"
	workout_type = request.form['workout_type']
	visits = request.form['visits']
	distance = request.form['distance']
	entry_date = datetime.datetime.now().strftime("%d/%m/%y")
	entry_time = datetime.datetime.now().strftime("%H:%M:%S")
	update_db(workout_id, workout_date, workout_type, visits, distance, entry_date, entry_time)
	df = view_db()
	return render_template('workout_results.html',  table = df.to_html(classes="table-striped"), 
		datetime_today = datetime_today(), datetime_now = datetime_now())

if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
