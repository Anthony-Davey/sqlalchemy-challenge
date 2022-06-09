from flask import Flask, jsonify, Response
import json
import numpy as np
import pandas as pd
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///C:\\Users\\Gamer\\Downloads/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station



# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Table of Contents <br/><br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    latest_date = "2017-08-23"
    twelve_months_precip = dt.date(2016,8,23)
    precip_query = session.query(measurement.date, func.avg(measurement.prcp)).\
                    filter(measurement.date >= twelve_months_precip).all()

    precip_dict = {Date: Precipitation for Date, Precipitation in precip_query}
    print(latest_date)
    print(twelve_months_precip)
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def route():
    active_stations = session.query(measurement.station, func.count(measurement.station)).\
            group_by(measurement.station).\
            order_by(func.count(measurement.station).desc()).all()
    
    station_dict = [station for station in active_stations]
    print(station)
    return Response(json.dumps(station_dict), mimetype='application/json')



if __name__ == "__main__":
    app.run(debug=True)
    

