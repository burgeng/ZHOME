from flask import Flask
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

endpoint = os.getenv("DATABASE_ENDPOINT")
port = os.getenv("DATABASE_PORT")
dbname = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

db_url = "postgresql://{}:{}@{}:{}/{}".format(user, password, endpoint, port, dbname)
connection = psycopg2.connect(db_url)

@app.get("/")
def index():
	return "CIS 550 Project"

@app.get("/checkdbconnection")
def db_conn_check():
	return "Connected to {}".format(db_url)

@app.get("/get_max_zhvi_by_metro")
def zhvi_metro_max():
	with connection:
		with connection.cursor() as cursor:
			cursor.execute('SELECT regionname, date, MAX(value) AS min_value FROM zhvi_processed_by_zhvi_metro_cleaned zhvi JOIN "Regions_cleaned" r ON zhvi.regionid=r.regionid GROUP BY regionname, date ORDER BY min_value DESC LIMIT 1')
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result


@app.get("/get_min_zhvi_by_metro")
def zhvi_metro_min():
	with connection:
		with connection.cursor() as cursor:
			cursor.execute('SELECT regionname, date, MIN(value) AS min_value FROM zhvi_processed_by_zhvi_metro_cleaned zhvi JOIN "Regions_cleaned" r ON zhvi.regionid=r.regionid GROUP BY regionname, date ORDER BY min_value ASC LIMIT 1')
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_mean_zhvi_by_metro")
def zhvi_metro_mean():
	with connection:
		with connection.cursor() as cursor:
			cursor.execute('SELECT regionname, AVG(value) AS avg_value FROM zhvi_processed_by_zhvi_metro_cleaned zhvi JOIN "Regions_cleaned" r ON zhvi.regionid=r.regionid GROUP BY regionname ORDER BY avg_value DESC LIMIT 50')
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result