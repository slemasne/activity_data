from flask import Flask, render_template, request, Response, make_response, send_file
from database import DataBase, TimeStmpToday
from plots import workout_plot, update_fig
import cStringIO
import datetime

app = Flask(__name__)
today = TimeStmpToday()
db = DataBase()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/db_reset',methods = ["POST","GET"])
def db_reset():
	db.create_table()
	return render_template('index.html')

@app.route('/sample',methods = ["POST","GET"])
def sample():
	df = db.load_legacy()
	return render_template('legacy_results.html',  table = df.to_html(classes="table-striped"), 
		datetime_today = today.today_date(), datetime_now = today.webpage_time())

@app.route("/to_csv", methods = ["POST","GET"])
def getWorkoutCSV():
	path = r"C:\Users\Stephen\Desktop\sp\flask\tyred\static\csv\workout_results.csv"
	csv =db. load_df().to_csv(path, encoding='utf-8')
	return send_file(path, as_attachment=True)

@app.route('/result', methods = ["POST","GET"])
def result():
	request.method == "POST"
	if not request.form['workout_date']:
		workout_date = today.today_date()
	else:
		workout_date = request.form['workout_date']
	workout_id = "TestID_1001"
	workout_type = request.form['workout_type']
	distance = request.form['distance']
	entry_date = today.today_date()
	entry_time = today.today_time()
	db.update_db(workout_id, workout_date, workout_type, distance, entry_date, entry_time)
	df = db.load_df()
	return render_template('workout_results.html',  table = df.to_html(classes="table-striped"), 
		datetime_today = today.today_date(), datetime_now = today.webpage_time())

@app.route('/plots')
def plots():
	update_fig()
	return render_template('to_plot.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
