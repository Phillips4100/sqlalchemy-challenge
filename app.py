import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request



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
        f"/api/v1.0/waihee_tobs<br/>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = {}
    prcp= engine.execute('SELECT measurement.date, measurement.prcp FROM measurement').fetchall()
    prcp_data= (Convert(prcp, precipitation))

    return jsonify(prcp_data)

@app.route("/api/v1.0/station")
def measurement():
    session = Session(engine)
    result = session.query(station.station, station.name).all()
    session.close()

    # Convert list of tuples into dict
    stats = {}
    stations = (Convert(result, stats))

    return jsonify(stations)

@app.route("/api/v1.0/waihee_tobs")
def tobs():
    waihee_tobs={}
    result1=engine.execute("SELECT date, tobs FROM measurement WHERE date > '2016-08-23' AND station = 'USC00519281'").fetchall()
    waihee_tobs_data = (Convert(result1, waihee_tobs))

    return jsonify(waihee_tobs_data)

@app.route("/api/v1.0/date")
def getdate():
    return """
        <html>
            <body>
                <h3>When is your trip?</h3>
                <form action = "/date">
                    Enter your start date (YYYY-MM-DD):<br>
                    <input type = 'text' name = 'start'><br>
                    <input type = 'submit' value = 'continue'>
                </form>
            </body>
        </html>
    """

@app.route("/api/v1.0/date<start>")

def get_temp():
    try:
        start = request.form.get('start')

    result2 = engine.execute(f'SELECT MAX(tobs) AS max,  AVG(tobs) AS avg, MIN(tobs) as min FROM measurement Where measurement.date > {Start}').fetchall()
    start_tobs = list(*result2)

    except:
    (f'Date not found')

    return jsonify(start_tobs)

if __name__ == '__main__':
    app.run(debug=True)