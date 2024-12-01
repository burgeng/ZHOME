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

db_url = "postgresql://{}:{}@{}:{}/{}".format(user, password, endpoint, port, dbname) # Construct DB URL string
connection = psycopg2.connect(db_url) # Establish connection to the DB

@app.get("/") # Root
def index():
	return "CIS 550 Project"

@app.get("/checkdbconnection") # Print the database url
def db_conn_check():
	status = ''
	conn_val = connection.closed # Should be 0 (False) if the connection is not closed (i.e. open)
	if conn_val == 0:
		status = 'Alive'
	else:
		status = 'Dead'
	return "DB URL: {} ; Status: {}".format(db_url, status)

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

#####
# Get ZHVI data by locality type and name
# Example URL: localhost:5000/get_zhvi?type=state&name=%27Pennsylvania%27 will get ZHVI data for Pennsylvania
#####
@app.get("/get_zhvi")
def get_zhvi():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	table_name = "zhvi_processed_by_zhvi_{}_cleaned".format(locality_type)
	print(table_name)
	with connection:
		with connection.cursor() as cursor:
			query = f'''
                SELECT date, regionname, regiontype, value AS ZHVI
				FROM {table_name} zhvi
				JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
				WHERE regionname = {locality_name}
				ORDER BY date ASC
            '''
			print(query)
			cursor.execute(query)
			rows = cursor.fetchall()
			# Get column names
			col_names = [desc[0] for desc in cursor.description]
			# Convert to list of dictionaries for JSON response
			result = [dict(zip(col_names, row)) for row in rows]
			return result

#####
# Get ZORI data by locality type and name
# Example URL: localhost:5000/get_zori?type=state&name=%27Pennsylvania%27 will get ZORI data for Pennsylvania
#####
@app.get("/get_zori")
def get_zori():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)
	print(table_name)
	with connection:
		with connection.cursor() as cursor:
			query = f'''
                SELECT date, regionname, regiontype, value AS ZORI
				FROM {table_name} zori
				JOIN "Regions_cleaned" rc ON zori.regionid = rc.regionid
				WHERE regionname = {locality_name}
				ORDER BY date ASC
            '''
			print(query)
			cursor.execute(query)
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

