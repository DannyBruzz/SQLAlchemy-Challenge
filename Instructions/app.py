import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all precipitation dates"""
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation) 
    


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations"""
    results = session.query(station.station).all()

    session.close()

 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a list of tobs"""
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == "USC00519281").\
    filter(measurement.date > '2016-08-23').\
    order_by(measurement.date).all()

    session.close()


    tob = []
    for date, tobs in results:
        tob_dict = {}
        tob_dict["date"] = date
        tob_dict["tobs"] = tobs
        tob.append(tob_dict)

    return jsonify(tob) 
    

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    """Return a list of start_date"""
   
    search_term = datetime.strptime(start, "%Y-%m-%d") 

    sel = [func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]
    results = session.query(*sel).\
    filter(measurement.date >= search_term).all()

    session.close()

    start_search = []
    for sel in results:
        start_search_dict = {}
        start_search_dict["Min"] = func.min(measurement.tobs)
        start_search_dict["Max"] = func.max(measurement.tobs)
        start_search_dict["Ave"] = func.avg(measurement.tobs)
        start_search.append(start_search_dict)

    start_search =list(np.ravel(results))

    return jsonify(start_search)

@app.route("/api/v1.0/<start>/<end>")
def period(start, end):
    session = Session(engine)
    """Return a list of start_date"""
   
    start_date = datetime.strptime(start, "%Y-%m-%d") 
    end_date = datetime.strptime(end, "%Y-%m-%d") 

    sel = [func.min(measurement.tobs), 
       func.max(measurement.tobs), 
       func.avg(measurement.tobs)]
    results = session.query(*sel).\
    filter(measurement.date >= start_date).\
    filter(measurement.date <= end_date).all()

    session.close()

    date_search = []
    for sel in results:
        date_search_dict = {}
        date_search_dict["Min"] = func.min(measurement.tobs)
        date_search_dict["Max"] = func.max(measurement.tobs)
        date_search_dict["Ave"] = func.avg(measurement.tobs)
        date_search.append(date_search_dict)

    date_search =list(np.ravel(results))

    return jsonify(date_search)


if __name__ == '__main__':
    app.run(debug=True)
