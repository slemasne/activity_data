from database import DataBase
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cStringIO, io
import os

def workout_plot():
	df = DataBase().load_df()
	img = io.BytesIO()
	df = df[["workout_id","workout_type"]]
	df = df.groupby("workout_type").count()
	df.rename(columns={"workout_id":"count_of_workout"})
	ax = df.plot(kind ="bar", title = "Count of workouts", legend=False)
	ax.set_ylabel("Count", fontsize=12)
	ax.set_xlabel("")
	fig = ax.get_figure()
	return fig

def update_fig():
	plt = workout_plot()
	path = os.getcwd()+ "\static\\" + "workout_plot.png"
  	plt.savefig(path)

