# 1. import 
import numpy as np 
import datetime as dt

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
 	    f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"1.Date and precipitation values from 2016-08-23 to 2017-08-23:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"2.List of stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"3.Date and temperature values from 2016-08-23 to 2017-08-23:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"4. Statistics for combined stations. Enter start date in form 'yyyy', 'yyyy-mm', or 'yyyy-mm-dd':<br/>"
        f"/api/v1.0/start<br/>"
        f"5. Statistics for combined stations. Enter start and end date in form 'yyyy', 'yyyy-mm', or 'yyyy-mm-dd':<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago)

    precipitation_dictionary = [{row[0]: row[1]} for row in last_12]
    precipitation_list = list(np.ravel(precipitation_dictionary))
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    stations_list = session.query(Station.station).all()
    list_stations = list(np.ravel(stations_list))

    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    date_tobs= session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()
    only_tobs = list(np.ravel([row[1] for row in date_tobs]))
    return jsonify(only_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    temp_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    temp_dict = [[{"TMIN" : row[0]}, {"TMAX" : row[1]}, {"TAVG" : row[2]}] for row in temp_start]
    temp_list = list(np.ravel(temp_dict))
    return jsonify (temp_list)
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    temp_startend = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    temp2_dict = [[{"TMIN" : row[0]}, {"TMAX" : row[1]}, {"TAVG" : row[2]}] for row in temp_startend]
    temp2_list = list(np.ravel(temp2_dict))
    return jsonify (temp2_list)

if __name__ == '__main__':
    app.run(debug=True)