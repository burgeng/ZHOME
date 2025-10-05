from flask import Flask, request
import mysql.connector
from mysql.connector import pooling
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

#connection = mysql.connector.connect(
#    host=endpoint,
#    port=port,
#    user=user,
#    password=password,
#    database=dbname
#)

cnpool = pooling.MySQLConnectionPool(
	host=endpoint,
    port=port,
    user=user,
    password=password,
    database=dbname,
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
)

@app.get("/") # Root
def index():
    return "ZHOME: The Zillow Housing Overview and Market Explorer"

@app.get("/checkdbconnection")
def db_conn_check():
    try:
        conn = cnpool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")  # simple check query
        cur.fetchone()
        conn.close()
        status = "Alive"
    except Exception as e:
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

    connection = cnpool.get_connection()
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
        print('Get localities ZHVI', rows)

        cur.execute(f"SELECT COUNT(DISTINCT regionid) FROM {table_name}")
        total_count = cur.fetchone()[0]

        response = {
            "options": [{"regionname": row[0], "state": row[1]} for row in rows],
            "totalPages": (total_count + limit - 1) // limit
        }

        return response
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if connection is not None and connection.is_connected():
            connection.close()  # returns it to the pool

@app.get("/get_localities_zori")
def get_states_zori():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)
    
	connection = cnpool.get_connection()
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
	finally:
		if connection is not None and connection.is_connected():
			connection.close()  # returns it to the pool

@app.get("/get_localities_zhvf")
def get_states_zhvf():
	locality_type = request.args.get("type")
	page = int(request.args.get("page", 1))  # Default to page 1
	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
	offset = (page - 1) * limit  # Calculate OFFSET

	table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)
    
	connection = cnpool.get_connection()
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
		print(rows)

		cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
		total_count = cursor.fetchone()[0]
		response = {
		"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
		"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
		}
		return response
	except Exception as e:
		return {"error": str(e)}, 500
	finally:
		if connection is not None and connection.is_connected():
			connection.close()  # returns it to the pool

@app.get("/get_localities_mhi")
def get_localities_mhi():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    if locality_type not in ["state", "county", "metro", "city", "zip", "neighborhood"]:
        return {"error": "Invalid locality type"}, 400

    # Convert 'metro' to 'msa' 
    if locality_type == "metro":
        locality_type = "msa"

    connection = cnpool.get_connection()
    cursor = connection.cursor()
    try:
        if locality_type == "msa":
            # --- METRO / MSA ---
            query = """
                SELECT DISTINCT rc.regionname, rc.statename
                FROM mhi_processed_by_metro_cleaned mhi
                JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid
                WHERE rc.regiontype = %s
                ORDER BY rc.regionname ASC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(DISTINCT rc.regionid)
                FROM mhi_processed_by_metro_cleaned mhi
                JOIN Regions_cleaned rc ON mhi.regionid = rc.regionid
                WHERE rc.regiontype = %s
            """, (locality_type,))
            total_count = cursor.fetchone()[0]

        elif locality_type == "state":
            # --- STATE ---
            query = """
                SELECT DISTINCT rc.statename
                FROM Regions_cleaned rc
                WHERE rc.regiontype = 'state'
                ORDER BY rc.statename ASC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(DISTINCT rc.statename)
                FROM Regions_cleaned rc
                WHERE rc.regiontype = 'state'
            """)
            total_count = cursor.fetchone()[0]

        else:
            return {"error": f"Locality type '{locality_type}' not implemented"}, 400

        # Build JSON response
        # For states: first and second column are both the state abbrev
        options = [{"regionname": r[0], "state": r[0]} for r in rows]

        return {
            "options": options,
            "totalPages": (total_count + limit - 1) // limit
        }

    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cursor.close()
        connection.close()

@app.get("/get_localities_newConstructionSales")
def get_localities_newConstruction_sales():
    locality_type = request.args.get("type")
    if locality_type != "metro":
        return {"error": "Only 'metro' is supported for new construction sales"}, 400

    # normalize to match Regions_cleaned
    locality_type = "msa"

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    table_name = "newconsales_processed_by_metro_cleaned"

    connection = cnpool.get_connection()
    cur = connection.cursor()
    try:
        # ---- METRO / MSA ----
        query = f"""
            SELECT DISTINCT rc.regionname, rc.statename
            FROM {table_name} sales
            JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
            WHERE rc.regiontype = %s
            ORDER BY rc.regionname ASC
            LIMIT %s OFFSET %s
        """
        cur.execute(query, (locality_type, limit, offset))
        rows = cur.fetchall()

        cur.execute(f"""
            SELECT COUNT(DISTINCT rc.regionid)
            FROM {table_name} sales
            JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
            WHERE rc.regiontype = %s
        """, (locality_type,))
        total_count = cur.fetchone()[0]

        return {
            "options": [{"regionname": r[0], "state": r[1]} for r in rows],
            "totalPages": (total_count + limit - 1) // limit
        }

    except Exception as e:
        print(e)
        return {"error": str(e)}, 500
    finally:
        cur.close()
        connection.close()



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

	connection = cnpool.get_connection()
	cursor = connection.cursor() 

	print(locality_type)
	if locality_type == 'state':
		query = f'''
		SELECT date, regionname, regiontype, value AS ZHVI
		FROM {table_name} zhvi
		JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
		WHERE regionname = %s AND regiontype = %s
		ORDER BY date ASC
		'''
		cursor.execute(query, (locality_name, locality_type))
		rows = cursor.fetchall()
		print("ZHVI Data: ", rows)
		col_names = [desc[0] for desc in cursor.description]
		result = [dict(zip(col_names, row)) for row in rows]
		return result
	else:
		query = f'''
			SELECT date, regionname, regiontype, value AS ZHVI
			FROM {table_name} zhvi
			JOIN Regions_cleaned rc ON zhvi.regionid = rc.regionid
			WHERE regionname = %s AND regiontype = %s AND rc.statename = %s
			ORDER BY date ASC
		'''
		cursor.execute(query, (locality_name, locality_type, state_name))
		rows = cursor.fetchall()
		print("ZHVI Data: ", rows)
		col_names = [desc[0] for desc in cursor.description]
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

    table_name = f"zori_processed_by_zori_{locality_type}_cleaned"
    if locality_type == 'metro':
        locality_type = 'msa'

    connection = cnpool.get_connection()
    cursor = connection.cursor()
    try:
        query = f'''
            SELECT date, regionname, regiontype, value AS ZORI
            FROM {table_name} zori
            JOIN Regions_cleaned rc ON zori.regionid = rc.regionid
            WHERE regionname = %s AND regiontype = %s AND statename = %s
            ORDER BY date ASC
        '''
        cursor.execute(query, (locality_name, locality_type, state_name))
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(col_names, row)) for row in rows]
        return result
    finally:
        cursor.close()
        connection.close()   # <-- returns to pool


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

    # Build table name
    table_name = f"zhvf_by_zhvf_{locality_type}_cleaned"
    if locality_type == 'metro':
        locality_type = 'msa'

    # --- FIX: get a pooled connection and ensure it is always released ---
    connection = cnpool.get_connection()
    cursor = connection.cursor()
    try:
        query = f'''
            SELECT month, quarter, year
            FROM {table_name} zhvf
            JOIN Regions_cleaned rc ON zhvf.regionid = rc.regionid
            WHERE regionname = %s AND regiontype = %s
            ORDER BY basedate ASC
        '''
        cursor.execute(query, (locality_name, locality_type))
        rows = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(col_names, row)) for row in rows]

        return result
    finally:
        cursor.close()
        connection.close() 

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

	connection = cnpool.get_connection()
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
	print(rows)
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

	connection = cnpool.get_connection()
	cursor = connection.cursor() 

	if locality_type == 'metro':
		query = f'''
			SELECT rc.regionname, date, value AS count
			FROM forsalelistings_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE regionname= '{locality_name}'
			ORDER BY date ASC
			'''
	# Similar to above, get average home sales for all metros in a state
	elif locality_type == 'state':
		query = f'''
			SELECT statename, date, AVG(CAST(value AS float)) AS count
			FROM forsalelistings_processed_by_metro_cleaned sales
			JOIN Regions_cleaned rc ON sales.regionid = rc.regionid
			WHERE statename = '{locality_name}'
			GROUP BY statename, date
			ORDER BY date ASC
			'''
	print(query)
	cursor.execute(query)
	rows = cursor.fetchall()
	print(rows)
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
	
	connection = cnpool.get_connection()
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
	print(rows)
	# Get column names
	col_names = [desc[0] for desc in cursor.description]
	# Convert to list of dictionaries for JSON response
	result = [dict(zip(col_names, row)) for row in rows]
	return result

