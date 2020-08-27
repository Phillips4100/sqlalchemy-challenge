import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#for converting lists of tuples to dictionarys
def Convert(tup, di): 
    di = dict(tup) 
    return di

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation = {}
    prcp= engine.execute('SELECT measurement.date, measurement.prcp FROM measurement').fetchall()
    prcp_data= (Convert(prcp, precipitation))

    return jsonify(prcp_data)

@app.route("/api/v1.0/station")
def measurement():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(station.station, station.name).all()
    session.close()

    # Convert list of tuples into dict
    stats = {}
    stations = (Convert(results, stats))

    return jsonify(stations)



if __name__ == '__main__':
    app.run(debug=True)