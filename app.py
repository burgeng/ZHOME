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

@app.get("/get_zhvi_metro")
def zhvi_metro():
	with connection:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM zhvi_processed_by_zhvi_metro_cleaned")
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result