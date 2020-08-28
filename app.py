import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

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
    return """
         <html>
             <body>
                 <h3>Available Routes:</h3>
                 <a href="http://127.0.0.1:5000/api/v1.0/precipitation" target="_blank">/api/v1.0/precipitation:</a><a1>  --Returns all precipitation measurments</a1><br>
                 <a href="http://127.0.0.1:5000/api/v1.0/station" target="_blank">/api/v1.0/station</a><a1>  --Returns all measurment stations.</a1><br>
                 <a href="http://127.0.0.1:5000/api/v1.0/waihee_tobs" target="_blank">/api/v1.0/waihee_tobs</a><a1>  --Returns date and temperature observations of the most active station for the last year of data.</a1><br>
                 <a>/api/v1.0/date/"(YYYY-MM-DD)</a><a1>  --Returns the temperature Average Maximum and Minimums for all dates greater than and equal to the date given</a1><br>
                 <a>/api/v1.0/date/"(YYYY-MM-DD)"/"(YYYY-MM-DD)</a><a1>  --Returns the temperature Average Maximum and Minimums for dates between the start and end date. </a1>
             </body>
         </html>
     """

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = {}
    prcp= engine.execute('SELECT measurement.date, measurement.prcp FROM measurement').fetchall()
    prcp_data= (Convert(prcp, precipitation))

    return jsonify(prcp_data)

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)
    result = session.query(station.station, station.name).all()
    session.close()

    # Convert list of tuples into dict
    stats = {}
    station_list = (Convert(result, stats))

    return jsonify(station_list)

@app.route("/api/v1.0/waihee_tobs")
def tobs():
    waihee_tobs={}
    result1=engine.execute("SELECT date, tobs FROM measurement WHERE date > '2016-08-23' AND station = 'USC00519281'").fetchall()
    waihee_tobs_data = (Convert(result1, waihee_tobs))

    return jsonify(waihee_tobs_data)

@app.route("/api/v1.0/date/<start>")
def tstart(start):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).order_by(measurement.date.desc()).all()

    session.close()
  
    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}

    return jsonify(dict)

@app.route("/api/v1.0/date/<start>/<end>")
def tstartend(start,end):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).order_by(measurement.date.desc()).all()

    session.close()

    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}

    return jsonify(dict)

if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/api/v1.0/date/<start>")
# def get_temp(start):
   
#     # start_date = request.form.get('start')
#     start_dt = datetime.strptime(start, '%Y-%m-%d')

#     result2 = engine.execute(SELECT MAX(measurment.tobs),  AVG(measurement.tobs), MIN(measurement.tobs) FROM measurement WHERE measurement.date >= start_dt GROUP BY measurement.date).fetchall()
#     start_tobs = list(*result2)
#     return jsonify(start_tobs)

    # request.form['start']
    # start = request.args.get('start')

# @app.route("/api/v1.0/date")
# def getdate():
#     return """
#         <html>
#             <body>
#                 <h3>When is your trip?</h3>
#                 <form ="startdate" action="/api/v1.0/date/" method="GET">
#                     Enter your start date (YYYY-MM-DD):<br>
#                     <input name = 'start'><br>
#                     <input type = 'submit' value = 'continue'>
#                 </form>
#             </body>
#         </html>
#     """
                # <form action = "/date/" >