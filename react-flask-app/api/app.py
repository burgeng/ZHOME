from flask import Flask, request
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

@app.get("/get_localities_zhvi")
def get_states_zhvi():
	locality_type = request.args.get('type')
	if locality_type.lower()=='metro':
		locality_type='msa'
	else:
		locality_type = locality_type.lower()
	print('Got type {}'.format(locality_type))
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT DISTINCT regionname
				FROM "Regions_cleaned"
				WHERE regiontype = %s
            '''
			cursor.execute(query, (locality_type,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

## TODO: Modify ZHVI routes to include locality type and locality name paramerts, one route for each data type
##			That way, it's easier from the frontend to handle user defined params.

@app.get("/get_zhvi_byState/<state>")
def get_zhvi_byState(state):
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT *
				FROM zhvi_processed_by_zhvi_state_cleaned zhvi
				JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
				WHERE regionname = %s
				ORDER BY date ASC
            '''
			cursor.execute(query, (state,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_zhvi_byCounty/<county>")
def get_zhvi_byCounty(county):
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT *
				FROM zhvi_processed_by_zhvi_county_cleaned zhvi
				JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
				WHERE regionname = %s
				ORDER BY date ASC
            '''
			cursor.execute(query, (county,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_zhvi_byMetro/<metro>")
def get_zhvi_byMetro(metro):
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT *
				FROM zhvi_processed_by_zhvi_metro_cleaned zhvi
				JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
				WHERE regionname = %s
				ORDER BY date ASC
            '''
			cursor.execute(query, (metro,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result


@app.get("/get_zhvi_zori_byMetro/<Metro>")
def get_zhvi_zori_byMetro(metro):
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT * 
                FROM (
                    SELECT 
                        zori.RegionID, 
                        zori.date, 
                        zhvi.value AS ZHVI, 
                        zori.value AS ZORI 
                    FROM 
                        zori_processed_by_zori_city_cleaned zori 
                    JOIN 
                        zhvi_processed_by_zhvi_city_cleaned zhvi 
                    ON 
                        zori.RegionID = zhvi.RegionID 
                        AND zori.date = zhvi.date 
                    ORDER BY date ASC
                ) AS t 
                JOIN 
                    "Regions_cleaned" rc 
                ON 
                    rc.RegionID = t.RegionID 
                WHERE regionname = %s
                ORDER BY date ASC
            '''
			cursor.execute(query, (city,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_zhvi_zori_byCity/<city>")
def get_zhvi_zori_byCity(city):
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT * 
                FROM (
                    SELECT 
                        zori.RegionID, 
                        zori.date, 
                        zhvi.value AS ZHVI, 
                        zori.value AS ZORI 
                    FROM 
                        zori_processed_by_zori_city_cleaned zori 
                    JOIN 
                        zhvi_processed_by_zhvi_city_cleaned zhvi 
                    ON 
                        zori.RegionID = zhvi.RegionID 
                        AND zori.date = zhvi.date 
                    ORDER BY date ASC
                ) AS t 
                JOIN 
                    "Regions_cleaned" rc 
                ON 
                    rc.RegionID = t.RegionID 
                WHERE regionname = %s
                ORDER BY date ASC
            '''
			cursor.execute(query, (city,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_zhvi_zori_byCounty/<county>")
def get_zhvi_zori_byCounty(county):
	print(f"Received county: {county}")
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT * 
                FROM (
                    SELECT 
                        zori.RegionID, 
                        zori.date, 
                        zhvi.value AS ZHVI, 
                        zori.value AS ZORI 
                    FROM 
                        zori_processed_by_zori_county_cleaned zori 
                    JOIN 
                        zhvi_processed_by_zhvi_county_cleaned zhvi 
                    ON 
                        zori.RegionID = zhvi.RegionID 
                        AND zori.date = zhvi.date 
                    ORDER BY date ASC
                ) AS t 
                JOIN 
                    "Regions_cleaned" rc 
                ON 
                    rc.RegionID = t.RegionID 
                WHERE regionname = %s
                ORDER BY date ASC
            '''
			cursor.execute(query, (county,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

@app.get("/get_zhvi_zori_byZIP/<zip_code>")
def get_zhvi_zori_byZIP(zip_code):
	print(f"Received county: {zip_code}")
	with connection:
		with connection.cursor() as cursor:
			query = '''
                SELECT * 
                FROM (
                    SELECT 
                        zori.RegionID, 
                        zori.date, 
                        zhvi.value AS ZHVI, 
                        zori.value AS ZORI 
                    FROM 
                        zori_processed_by_zori_zip_cleaned zori 
                    JOIN 
                        zhvi_processed_by_zhvi_zip_cleaned zhvi 
                    ON 
                        zori.RegionID = zhvi.RegionID 
                        AND zori.date = zhvi.date 
                    ORDER BY date ASC
                ) AS t 
                JOIN 
                    "Regions_cleaned" rc 
                ON 
                    rc.RegionID = t.RegionID 
                WHERE regionname = %s
                ORDER BY date ASC
            '''
			cursor.execute(query, (zip_code,))
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

