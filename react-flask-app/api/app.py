from flask import Flask, request
import mysql.connector
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

endpoint = os.getenv("DATABASE_ENDPOINT")
port = int(os.getenv("DATABASE_PORT"))
dbname = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

print(f"Endpoint: {endpoint}\nPort: {port}\nDatabase name: {dbname}\nUser: {user}")

#db_path = os.getenv("SQLITE_DB_PATH", "../../preprocessing/data/housing.db")
#connection = sqlite3.connect(db_path, check_same_thread=False)
#connection.row_factory = sqlite3.Row  # Optional: rows as dict-like objects

connection = mysql.connector.connect(
    host=endpoint,
    port=port,
    user=user,
    password=password,
    database=dbname
)

@app.get("/") # Root
def index():
    return "ZHOME: The Zillow Housing Overview and Market Explorer"

@app.get("/checkdbconnection")
def db_conn_check():
    try:
        conn = connection
        cur = conn.cursor()
        cur.execute("SELECT 1;")  # simple check query
        cur.fetchone()
        conn.close()
        status = "Alive"
    except sqlite3.Error as e:
        status = f"Dead ({e})"
    return {"Status": status}

########## Accessory routes for frontend lists ##########
@app.get("/get_localities_zhvi")
def get_states_zhvi():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))   # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = f"zhvi_processed_by_zhvi_{locality_type}_cleaned"

    if locality_type == "metro":
        locality_type = "msa"

    cur = connection.cursor()

    try:
        if locality_type == "state":
            query = f"""
            SELECT DISTINCT regionname, regionname
            FROM {table_name} zhvi
                JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
            WHERE regiontype = %s
            ORDER BY regionname ASC
            LIMIT %s OFFSET %s
            """
        else:
            query = f"""
            SELECT DISTINCT regionname, statename
            FROM {table_name} zhvi
                JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
            WHERE regiontype = %s
            ORDER BY regionname ASC
            LIMIT %s OFFSET %s
            """

        cur.execute(query, (locality_type, limit, offset))
        rows = cur.fetchall()

        cur.execute(f"SELECT COUNT(DISTINCT regionid) FROM {table_name}")
        total_count = cur.fetchone()[0]

        response = {
            "options": [{"regionname": row[0], "state": row[1]} for row in rows],
            "totalPages": (total_count + limit - 1) // limit
        }

        return response
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/get_localities_zori")
def get_states_zori():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)

	cursor = connection.cursor() 

	if locality_type == "metro":
		locality_type = "msa"

	try:
		query = f'''
		SELECT DISTINCT regionname, statename
		FROM {table_name} zori 
			JOIN Regions_cleaned rc ON zori.regionid = rc.regionid 
		WHERE regiontype = %s
		ORDER BY regionname ASC
		LIMIT %s OFFSET %s
		'''
		cursor.execute(query, (locality_type, limit, offset))
		rows = cursor.fetchall()

		cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
		total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
		return response
	except Exception as e:
		return {"error": str(e)}, 500

@app.get("/get_localities_zhvf")
def get_states_zhvf():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)

	cursor = connection.cursor() 

	if locality_type == "metro":
		locality_type = "msa"

	try:
		query = f'''
		SELECT DISTINCT regionname, statename
		FROM {table_name} zhvf 
			JOIN Regions_cleaned rc ON zhvf.regionid = rc.regionid 
		WHERE regiontype = %s
		ORDER BY regionname ASC
		LIMIT %s OFFSET %s
		'''
		cursor.execute(query, (locality_type, limit, offset))
		rows = cursor.fetchall()

		cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
		total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
		return response
	except Exception as e:
		return {"error": str(e)}, 500

@app.get("/get_localities_mhi")
def get_states_mhi():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	if locality_type == "metro":
		locality_type = "msa"
	rows=[]
	total_count=0

	cursor = connection.cursor() 
	
	try:
		# We can't just access different tables here, so we will have to have different queries
		if locality_type == 'msa':
			query = f'''
			SELECT DISTINCT regionname, statename
			FROM mhi_processed_by_metro_cleaned mhi 
				JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid 
			WHERE regiontype = %s
			ORDER BY regionname ASC
			LIMIT %s OFFSET %s
			'''
			cursor.execute(query, (locality_type, limit, offset))
			rows = cursor.fetchall()
			print(rows)
			cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM mhi_processed_by_metro_cleaned')
			total_count = cursor.fetchone()[0]

		elif locality_type == 'state':
			query = f'''
			SELECT DISTINCT statename, statename
			FROM mhi_processed_by_metro_cleaned mhi
				JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid
			ORDER BY statename ASC
			LIMIT %s OFFSET %s
			'''
			cursor.execute(query, (limit, offset))
			rows = cursor.fetchall()
			print(rows)
			cursor.execute(f'SELECT COUNT(DISTINCT statename) FROM mhi_processed_by_metro_cleaned mhi JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid ')
			total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
	except Exception as e:
		return {"error": str(e)}, 500
	
	return response

@app.get("/get_localities_sales")
def get_states_sales():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	if locality_type == "metro":
		locality_type = "msa"

	cursor = connection.cursor() 

	try:
		if locality_type == 'msa':
			query = f'''
			SELECT DISTINCT regionname, statename
			FROM sales_processed_by_metro_cleaned sales 
				JOIN Regions_cleaned rc ON sales.regionid = rc.regionid 
			WHERE regiontype = '{locality_type}'
			ORDER BY regionname ASC
			LIMIT {limit} OFFSET {offset}
			'''
		elif locality_type == 'state':
			query = f'''
			SELECT DISTINCT statename, statename
			FROM sales_processed_by_metro_cleaned sales
				JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			ORDER BY statename ASC
			LIMIT {limit} OFFSET {offset}
			'''
		cursor.execute(query)
		rows = cursor.fetchall()

		cursor.execute('SELECT COUNT(DISTINCT regionid) FROM sales_processed_by_metro_cleaned')
		total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
		return response
	except Exception as e:
		return {"error": str(e)}, 500

@app.get("/get_localities_newConstructionSales")
def get_states_newConstructionSales():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	if locality_type == "metro":
		locality_type = "msa"

	cursor = connection.cursor() 

	try:
		if locality_type == 'msa':
			query = f'''
			SELECT DISTINCT regionname, statename
			FROM newconsales_processed_by_metro_cleaned sales 
				JOIN Regions_cleaned rc ON sales.regionid = rc.regionid 
			WHERE regiontype = '{locality_type}'
			ORDER BY regionname ASC
			LIMIT {limit} OFFSET {offset}
			'''
		elif locality_type == 'state':
			query = f'''
			SELECT DISTINCT statename, statename
			FROM newconsales_processed_by_metro_cleaned sales
				JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			ORDER BY statename ASC
			LIMIT {limit} OFFSET {offset}
			'''
		cursor.execute(query)
		rows = cursor.fetchall()

		cursor.execute('SELECT COUNT(DISTINCT regionid) FROM newconsales_processed_by_metro_cleaned')
		total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
		return response
	except Exception as e:
		return {"error": str(e)}, 500


#####
# Get ZHVI data by locality type and name
# Example URL: localhost:5000/get_zhvi?type=state&name=%27Pennsylvania%27 will get ZHVI data for Pennsylvania
#####
@app.get("/get_zhvi")
def get_zhvi():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	state_name = request.args.get('state')
	
	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	table_name = "zhvi_processed_by_zhvi_{}_cleaned".format(locality_type)

	if locality_type == 'metro':
		locality_type = 'msa'

	cursor = connection.cursor() 

	print(locality_type)
	if locality_type == 'state': # In this case, the statename columns are null
		query = f'''
		SELECT date, regionname, regiontype, value AS ZHVI
		FROM {table_name} zhvi
		JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
		WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}'
		ORDER BY date ASC
		'''
	else:
		query = f'''
			SELECT date, regionname, regiontype, value AS ZHVI
			FROM {table_name} zhvi
			JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
			WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}' AND rc.statename = '{state_name}'
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
	state_name = request.args.get('state')
	
	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)

	if locality_type == 'metro':
		locality_type = 'msa'

	cursor = connection.cursor() 

	print(table_name)
	query = f'''
		SELECT date, regionname, regiontype, value AS ZORI
		FROM {table_name} zori
		JOIN Regions_cleaned rc ON zori.regionid = rc.regionid
		WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}' AND statename = '{state_name}'
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
# Get ZHVF data by locality type and name
# Example URL: localhost:5000/get_zhvf?type=state&name=%27Pennsylvania%27 will get ZHVF data for Pennsylvania
#####
@app.get("/get_zhvf")
def get_zhvf():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)

	if locality_type == 'metro':
		locality_type = 'msa'

	cursor = connection.cursor() 

	query = f'''
		SELECT month, quarter, year
		FROM {table_name} zhvf
		JOIN Regions_cleaned rc ON zhvf.regionid = rc.regionid
		WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}'
		ORDER BY basedate ASC
	'''
	print(query)
	cursor.execute(query)
	rows = cursor.fetchall()
	# Get column names
	col_names = [desc[0] for desc in cursor.description]
	# Convert to list of dictionaries for JSON response
	result = [dict(zip(col_names, row)) for row in rows]
	print(result)
	return result

#####
# Get MHI data by locality type and name
# Example URL: localhost:5000/get_zori?type=state&name=%27Pennsylvania%27 will get ZORI data for Pennsylvania
#####
@app.get("/get_mhi")
def get_mhi():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'metro']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	if locality_type == 'metro':
		locality_type == 'msa'

	cursor = connection.cursor() 

	if locality_type == 'metro':
		query = f'''
			SELECT rc.regionname, date, value AS mhi
			FROM mhi_processed_by_metro_cleaned mhi
			JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid
			WHERE regionname= '{locality_name}'
			ORDER BY date ASC
		'''
	# Since there is only a metro table for MHI, we can estimate the by-State values by averaging values for all metros in a state using a GROUP BY clause with AVG()
	elif locality_type == 'state':
		query = f'''
			SELECT statename, date, AVG(CAST(value AS float)) AS mhi
			FROM mhi_processed_by_metro_cleaned mhi
			JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid
			WHERE statename = '{locality_name}'
			GROUP BY statename, date
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
# Get home sale count data by locality type and name
#####
@app.get("/get_homesales")
def get_homesales():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'metro']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	if locality_type == 'metro':
		locality_type == 'msa'

	cursor = connection.cursor() 

	if locality_type == 'metro':
		query = f'''
			SELECT rc.regionname, date, value AS count
			FROM sales_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE regionname= '{locality_name}'
			ORDER BY date ASC
			'''
	# Similar to above, get average home sales for all metros in a state
	elif locality_type == 'state':
		query = f'''
			SELECT statename, date, AVG(CAST(value AS float)) AS count
			FROM sales_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE statename = '{locality_name}'
			GROUP BY statename, date
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
# Get new construction sale count data by locality type and name
#####
@app.get("/get_newConstructionSales")
def get_newConstructionSales():
	locality_type = request.args.get('type')
	locality_name = request.args.get('name')
	
	valid_locality_types = ['state', 'metro']
	if locality_type not in valid_locality_types:
		return {"error": "Invalid locality type"}, 400

	if locality_type == 'metro':
		locality_type == 'msa'
	
	cursor = connection.cursor() 

	if locality_type == 'metro':
		query = f'''
			SELECT rc.regionname, date, value AS count
			FROM newconsales_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE regionname= '{locality_name}'
			ORDER BY date ASC
			'''
	# Similar to above, get average home sales for all metros in a state
	elif locality_type == 'state':
		query = f'''
			SELECT statename, date, AVG(CAST(value AS float)) AS count
			FROM newconsales_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE statename = '{locality_name}'
			GROUP BY statename, date
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

