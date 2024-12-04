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
connection.autocommit = True

# @app.get("/") # Root
# def index():
# 	return "CIS 550 Project"

# @app.get("/checkdbconnection") # Print the database url
# def db_conn_check():
# 	status = ''
# 	conn_val = connection.closed # Should be 0 (False) if the connection is not closed (i.e. open)
# 	if conn_val == 0:
# 		status = 'Alive'
# 	else:
# 		status = 'Dead'
# 	return "DB URL: {} ; Status: {}".format(db_url, status)

# ########## Accessory routes for frontend lists ##########
# @app.get("/get_localities_zhvi")
# def get_states_zhvi():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	table_name = "zhvi_processed_by_zhvi_{}_cleaned".format(locality_type)

# 	if locality_type == "metro":
# 		locality_type = "msa"

# 	try:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'state':
# 				query = f'''
# 				SELECT DISTINCT regionname, regionname
# 				FROM {table_name} zhvi 
# 					JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid 
# 				WHERE regiontype = %s
# 				ORDER BY regionname ASC
# 				LIMIT %s OFFSET %s
# 				'''
# 			else:
# 				query = f'''
# 				SELECT DISTINCT regionname, statename
# 				FROM {table_name} zhvi 
# 					JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid 
# 				WHERE regiontype = %s
# 				ORDER BY regionname ASC
# 				LIMIT %s OFFSET %s
# 				'''
# 			cursor.execute(query, (locality_type, limit, offset))
# 			rows = cursor.fetchall()

# 			cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
# 			total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 			return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500


@app.route("/", methods=["GET"])  # Root
def index():
    return "CIS 550 Project"


@app.route("/checkdbconnection", methods=["GET"])  # Print the database URL
def db_conn_check():
    status = ''
    conn_val = connection.closed  # Should be 0 (False) if the connection is not closed (i.e. open)
    if conn_val == 0:
        status = 'Alive'
    else:
        status = 'Dead'
    return f"DB URL: {db_url} ; Status: {status}"


########## Accessory routes for frontend lists ##########
@app.route("/get_localities_zhvi", methods=["GET"])
def get_states_zhvi():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = f"zhvi_processed_by_zhvi_{locality_type}_cleaned"

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            if locality_type == 'state':
                query = f'''
                SELECT DISTINCT regionname, regionname
                FROM {table_name} zhvi 
                    JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid 
                WHERE regiontype = %s
                ORDER BY regionname ASC
                LIMIT %s OFFSET %s
                '''
            else:
                query = f'''
                SELECT DISTINCT regionname, statename
                FROM {table_name} zhvi 
                    JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid 
                WHERE regiontype = %s
                ORDER BY regionname ASC
                LIMIT %s OFFSET %s
                '''
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(DISTINCT regionid) FROM {table_name}")
            total_count = cursor.fetchone()[0]
            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


# @app.get("/get_localities_zori")
# def get_states_zori():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)

# 	if locality_type == "metro":
# 		locality_type = "msa"

# 	try:
# 		with connection.cursor() as cursor:
# 			query = f'''
# 			SELECT DISTINCT regionname, statename
# 			FROM {table_name} zori 
# 				JOIN "Regions_cleaned" rc ON zori.regionid = rc.regionid 
# 			WHERE regiontype = %s
# 			ORDER BY regionname ASC
# 			LIMIT %s OFFSET %s
# 			'''
# 			cursor.execute(query, (locality_type, limit, offset))
# 			rows = cursor.fetchall()

# 			cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
# 			total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 			return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500

# @app.get("/get_localities_zhvf")
# def get_states_zhvf():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)

# 	if locality_type == "metro":
# 		locality_type = "msa"

# 	try:
# 		with connection.cursor() as cursor:
# 			query = f'''
# 			SELECT DISTINCT regionname, statename
# 			FROM {table_name} zhvf 
# 				JOIN "Regions_cleaned" rc ON zhvf.regionid = rc.regionid 
# 			WHERE regiontype = %s
# 			ORDER BY regionname ASC
# 			LIMIT %s OFFSET %s
# 			'''
# 			cursor.execute(query, (locality_type, limit, offset))
# 			rows = cursor.fetchall()

# 			cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
# 			total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 			return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500

# @app.get("/get_localities_mhi")
# def get_states_mhi():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	if locality_type == "metro":
# 		locality_type = "msa"
# 	rows=[]
# 	total_count=0
# 	try:
# 		with connection.cursor() as cursor:
# 			# We can't just access different tables here, so we will have to have different queries
# 			if locality_type == 'msa':
# 				query = f'''
# 				SELECT DISTINCT regionname, statename
# 				FROM mhi_processed_by_metro_cleaned mhi 
# 					JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid 
# 				WHERE regiontype = %s
# 				ORDER BY regionname ASC
# 				LIMIT %s OFFSET %s
# 				'''
# 				cursor.execute(query, (locality_type, limit, offset))
# 				rows = cursor.fetchall()
# 				print(rows)
# 				cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM mhi_processed_by_metro_cleaned')
# 				total_count = cursor.fetchone()[0]

# 			elif locality_type == 'state':
# 				query = f'''
# 				SELECT DISTINCT statename, statename
# 				FROM mhi_processed_by_metro_cleaned mhi
# 					JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
# 				ORDER BY statename ASC
# 				LIMIT %s OFFSET %s
# 				'''
# 				cursor.execute(query, (limit, offset))
# 				rows = cursor.fetchall()
# 				print(rows)
# 				cursor.execute(f'SELECT COUNT(DISTINCT statename) FROM mhi_processed_by_metro_cleaned mhi JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid ')
# 				total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 		return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500



@app.route("/get_localities_zori", methods=["GET"])
def get_states_zori():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = f"zori_processed_by_zori_{locality_type}_cleaned"

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            query = f'''
            SELECT DISTINCT regionname, statename
            FROM {table_name} zori 
                JOIN "Regions_cleaned" rc ON zori.regionid = rc.regionid 
            WHERE regiontype = %s
            ORDER BY regionname ASC
            LIMIT %s OFFSET %s
            '''
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(DISTINCT regionid) FROM {table_name}")
            total_count = cursor.fetchone()[0]

            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_localities_zhvf", methods=["GET"])
def get_states_zhvf():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = f"zhvf_by_zhvf_{locality_type}_cleaned"

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            query = f'''
            SELECT DISTINCT regionname, statename
            FROM {table_name} zhvf 
                JOIN "Regions_cleaned" rc ON zhvf.regionid = rc.regionid 
            WHERE regiontype = %s
            ORDER BY regionname ASC
            LIMIT %s OFFSET %s
            '''
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute(f"SELECT COUNT(DISTINCT regionid) FROM {table_name}")
            total_count = cursor.fetchone()[0]

            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_localities_mhi", methods=["GET"])
def get_states_mhi():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    if locality_type == "metro":
        locality_type = "msa"
    rows = []
    total_count = 0
    try:
        with connection.cursor() as cursor:
            # We can't just access different tables here, so we will have to have different queries
            if locality_type == "msa":
                query = f'''
                SELECT DISTINCT regionname, statename
                FROM mhi_processed_by_metro_cleaned mhi 
                    JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid 
                WHERE regiontype = %s
                ORDER BY regionname ASC
                LIMIT %s OFFSET %s
                '''
                cursor.execute(query, (locality_type, limit, offset))
                rows = cursor.fetchall()

                cursor.execute(f"SELECT COUNT(DISTINCT regionid) FROM mhi_processed_by_metro_cleaned")
                total_count = cursor.fetchone()[0]

            elif locality_type == "state":
                query = f'''
                SELECT DISTINCT statename, statename
                FROM mhi_processed_by_metro_cleaned mhi
                    JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
                ORDER BY statename ASC
                LIMIT %s OFFSET %s
                '''
                cursor.execute(query, (limit, offset))
                rows = cursor.fetchall()

                cursor.execute(
                    f'''
                    SELECT COUNT(DISTINCT statename) 
                    FROM mhi_processed_by_metro_cleaned mhi 
                        JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
                    '''
                )
                total_count = cursor.fetchone()[0]

            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


# @app.get("/get_localities_sales")
# def get_states_sales():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	if locality_type == "metro":
# 		locality_type = "msa"

# 	try:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'msa':
# 				query = f'''
# 				SELECT DISTINCT regionname, statename
# 				FROM sales_processed_by_metro_cleaned sales 
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid 
# 				WHERE regiontype = '{locality_type}'
# 				ORDER BY regionname ASC
# 				LIMIT {limit} OFFSET {offset}
# 				'''
# 			elif locality_type == 'state':
# 				query = f'''
# 				SELECT DISTINCT statename, statename
# 				FROM sales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 				ORDER BY statename ASC
# 				LIMIT {limit} OFFSET {offset}
# 				'''
# 			cursor.execute(query)
# 			rows = cursor.fetchall()

# 			cursor.execute('SELECT COUNT(DISTINCT regionid) FROM sales_processed_by_metro_cleaned')
# 			total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 			return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500

# @app.get("/get_localities_newConstructionSales")
# def get_states_newConstructionSales():
# 	locality_type = request.args.get("type")
# 	page = int(request.args.get("page", 1))  # Default to page 1
# 	limit = int(request.args.get("limit", 10))  # Default to 10 records per page
# 	offset = (page - 1) * limit  # Calculate OFFSET

# 	if locality_type == "metro":
# 		locality_type = "msa"

# 	try:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'msa':
# 				query = f'''
# 				SELECT DISTINCT regionname, statename
# 				FROM newconsales_processed_by_metro_cleaned sales 
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid 
# 				WHERE regiontype = '{locality_type}'
# 				ORDER BY regionname ASC
# 				LIMIT {limit} OFFSET {offset}
# 				'''
# 			elif locality_type == 'state':
# 				query = f'''
# 				SELECT DISTINCT statename, statename
# 				FROM newconsales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 				ORDER BY statename ASC
# 				LIMIT {limit} OFFSET {offset}
# 				'''
# 			cursor.execute(query)
# 			rows = cursor.fetchall()

# 			cursor.execute('SELECT COUNT(DISTINCT regionid) FROM newconsales_processed_by_metro_cleaned')
# 			total_count = cursor.fetchone()[0]
# 			response = {
# 			"options": [{"regionname": row[0], "state": row[1]} for row in rows],  # Adjust based on your table structure
# 			"totalPages": (total_count + limit - 1) // limit  # Calculate total pages
# 	 		}
# 			return response
# 	except Exception as e:
# 		return {"error": str(e)}, 500


# #####
# # Get ZHVI data by locality type and name
# # Example URL: localhost:5000/get_zhvi?type=state&name=%27Pennsylvania%27 will get ZHVI data for Pennsylvania
# #####
# @app.get("/get_zhvi")
# def get_zhvi():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
# 	state_name = request.args.get('state')
	
# 	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	table_name = "zhvi_processed_by_zhvi_{}_cleaned".format(locality_type)

# 	if locality_type == 'metro':
# 		locality_type = 'msa'

# 	with connection:
# 		with connection.cursor() as cursor:
# 			print(locality_type)
# 			if locality_type == 'state': # In this case, the statename columns are null
# 				query = f'''
#                 SELECT date, regionname, regiontype, value AS ZHVI
# 				FROM {table_name} zhvi
# 				JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
# 				WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}'
# 				ORDER BY date ASC
#            		'''
# 			else:
# 				query = f'''
# 	                SELECT date, regionname, regiontype, value AS ZHVI
# 					FROM {table_name} zhvi
# 					JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
# 					WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}' AND rc.statename = '{state_name}'
# 					ORDER BY date ASC
# 	            '''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			return result


@app.route("/get_localities_sales", methods=["GET"])
def get_states_sales():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            if locality_type == 'msa':
                query = f'''
                SELECT DISTINCT regionname, statename
                FROM sales_processed_by_metro_cleaned sales 
                    JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid 
                WHERE regiontype = '{locality_type}'
                ORDER BY regionname ASC
                LIMIT {limit} OFFSET {offset}
                '''
            elif locality_type == 'state':
                query = f'''
                SELECT DISTINCT statename, statename
                FROM sales_processed_by_metro_cleaned sales
                    JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
                ORDER BY statename ASC
                LIMIT {limit} OFFSET {offset}
                '''
            cursor.execute(query)
            rows = cursor.fetchall()

            cursor.execute('SELECT COUNT(DISTINCT regionid) FROM sales_processed_by_metro_cleaned')
            total_count = cursor.fetchone()[0]
            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_localities_newConstructionSales", methods=["GET"])
def get_states_newConstructionSales():
    locality_type = request.args.get("type")
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            if locality_type == 'msa':
                query = f'''
                SELECT DISTINCT regionname, statename
                FROM newconsales_processed_by_metro_cleaned sales 
                    JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid 
                WHERE regiontype = '{locality_type}'
                ORDER BY regionname ASC
                LIMIT {limit} OFFSET {offset}
                '''
            elif locality_type == 'state':
                query = f'''
                SELECT DISTINCT statename, statename
                FROM newconsales_processed_by_metro_cleaned sales
                    JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
                ORDER BY statename ASC
                LIMIT {limit} OFFSET {offset}
                '''
            cursor.execute(query)
            rows = cursor.fetchall()

            cursor.execute('SELECT COUNT(DISTINCT regionid) FROM newconsales_processed_by_metro_cleaned')
            total_count = cursor.fetchone()[0]
            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_zhvi", methods=["GET"])
def get_zhvi():
    locality_type = request.args.get('type')
    locality_name = request.args.get('name')
    state_name = request.args.get('state')
    
    valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
    if locality_type not in valid_locality_types:
        return {"error": "Invalid locality type"}, 400

    table_name = f"zhvi_processed_by_zhvi_{locality_type}_cleaned"

    if locality_type == 'metro':
        locality_type = 'msa'

    with connection:
        with connection.cursor() as cursor:
            print(locality_type)
            if locality_type == 'state':  # In this case, the statename columns are null
                query = f'''
                SELECT date, regionname, regiontype, value AS ZHVI
                FROM {table_name} zhvi
                JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
                WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}'
                ORDER BY date ASC
                '''
            else:
                query = f'''
                SELECT date, regionname, regiontype, value AS ZHVI
                FROM {table_name} zhvi
                JOIN "Regions_cleaned" rc ON zhvi.regionid = rc.regionid
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
# @app.get("/get_zori")
# def get_zori():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
# 	state_name = request.args.get('state')
	
# 	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)

# 	if locality_type == 'metro':
# 		locality_type = 'msa'

# 	print(table_name)
# 	with connection:
# 		with connection.cursor() as cursor:
# 			query = f'''
#                 SELECT date, regionname, regiontype, value AS ZORI
# 				FROM {table_name} zori
# 				JOIN "Regions_cleaned" rc ON zori.regionid = rc.regionid
# 				WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}' AND statename = '{state_name}'
# 				ORDER BY date ASC
#             '''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			return result

# #####
# # Get ZHVF data by locality type and name
# # Example URL: localhost:5000/get_zhvf?type=state&name=%27Pennsylvania%27 will get ZHVF data for Pennsylvania
# #####
# @app.get("/get_zhvf")
# def get_zhvf():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
	
# 	valid_locality_types = ['state', 'county', 'metro', 'city', 'zip', 'neighborhood']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)

# 	if locality_type == 'metro':
# 		locality_type = 'msa'

# 	with connection:
# 		with connection.cursor() as cursor:
# 			query = f'''
#                 SELECT month, quarter, year
# 				FROM {table_name} zhvf
# 				JOIN "Regions_cleaned" rc ON zhvf.regionid = rc.regionid
# 				WHERE regionname = '{locality_name}' AND regiontype = '{locality_type}'
# 				ORDER BY basedate ASC
#             '''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			print(result)
# 			return result

# #####
# # Get MHI data by locality type and name
# # Example URL: localhost:5000/get_zori?type=state&name=%27Pennsylvania%27 will get ZORI data for Pennsylvania
# #####
# @app.get("/get_mhi")
# def get_mhi():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
	
# 	valid_locality_types = ['state', 'metro']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	if locality_type == 'metro':
# 		locality_type == 'msa'

# 	with connection:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'metro':
# 				query = f'''
# 					SELECT rc.regionname, date, value AS mhi
# 					FROM mhi_processed_by_metro_cleaned mhi
# 					JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
# 					WHERE regionname= '{locality_name}'
# 					ORDER BY date ASC
# 	            '''
# 	        # Since there is only a metro table for MHI, we can estimate the by-State values by averaging values for all metros in a state using a GROUP BY clause with AVG()
# 			elif locality_type == 'state':
# 				query = f'''
# 					SELECT statename, date, AVG(CAST(value AS float)) AS mhi
# 					FROM mhi_processed_by_metro_cleaned mhi
# 					JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
# 					WHERE statename = '{locality_name}'
# 					GROUP BY statename, date
# 					ORDER BY date ASC
# 	            '''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			return result

# #####
# # Get home sale count data by locality type and name
# #####
# @app.get("/get_homesales")
# def get_homesales():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
	
# 	valid_locality_types = ['state', 'metro']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	if locality_type == 'metro':
# 		locality_type == 'msa'

# 	with connection:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'metro':
# 				query = f'''
# 					SELECT rc.regionname, date, value AS count
# 					FROM sales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 					WHERE regionname= '{locality_name}'
# 					ORDER BY date ASC
# 		         	'''
# 		    # Similar to above, get average home sales for all metros in a state
# 			elif locality_type == 'state':
# 				query = f'''
# 					SELECT statename, date, AVG(CAST(value AS float)) AS count
# 					FROM sales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 					WHERE statename = '{locality_name}'
# 					GROUP BY statename, date
# 					ORDER BY date ASC
# 		         	'''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			return result

# #####
# # Get new construction sale count data by locality type and name
# #####
# @app.get("/get_newConstructionSales")
# def get_newConstructionSales():
# 	locality_type = request.args.get('type')
# 	locality_name = request.args.get('name')
	
# 	valid_locality_types = ['state', 'metro']
# 	if locality_type not in valid_locality_types:
# 		return {"error": "Invalid locality type"}, 400

# 	if locality_type == 'metro':
# 		locality_type == 'msa'

# 	with connection:
# 		with connection.cursor() as cursor:
# 			if locality_type == 'metro':
# 				query = f'''
# 					SELECT rc.regionname, date, value AS count
# 					FROM newconsales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 					WHERE regionname= '{locality_name}'
# 					ORDER BY date ASC
# 		         	'''
# 		    # Similar to above, get average home sales for all metros in a state
# 			elif locality_type == 'state':
# 				query = f'''
# 					SELECT statename, date, AVG(CAST(value AS float)) AS count
# 					FROM newconsales_processed_by_metro_cleaned sales
# 					JOIN "Regions_cleaned" rc ON sales.regionid = rc.regionid
# 					WHERE statename = '{locality_name}'
# 					GROUP BY statename, date
# 					ORDER BY date ASC
# 		         	'''
# 			print(query)
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			# Get column names
# 			col_names = [desc[0] for desc in cursor.description]
# 			# Convert to list of dictionaries for JSON response
# 			result = [dict(zip(col_names, row)) for row in rows]
# 			return result



# @app.route("/get_forecast_data", methods=["GET"])
# def get_forecast_data():
#     # Get query parameters
#     region_name = request.args.get("regionname")
#     region_type = request.args.get("regiontype")
    
#     if not region_name or not region_type:
#         return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

#     try:
#         with connection.cursor() as cursor:
#             # SQL query to join tables and filter based on regionname and regiontype
#             query = '''
#             SELECT 
#                 rc.regionid, 
#                 rc.regionname, 
#                 rc.regiontype, 
#                 fl.date, 
#                 fl.value 
#             FROM 
#                 public."Regions_cleaned" rc
#             JOIN 
#                 public.forsalelistings_processed_by_metro_cleaned fl
#             ON 
#                 rc.regionid = fl.regionid
#             WHERE 
#                 rc.regionname = %s AND rc.regiontype = %s
#             ORDER BY 
#                 fl.date ASC
#             '''
#             # Execute query with parameters
#             cursor.execute(query, (region_name, region_type))
#             rows = cursor.fetchall()

#             # Get column names
#             col_names = [desc[0] for desc in cursor.description]

#             # Format results as a list of dictionaries
#             result = [dict(zip(col_names, row)) for row in rows]
#             return {"data": result}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500
    


# @app.get("/get_mhi_data")
# def get_mhi_data():
#     # Get query parameters
#     region_name = request.args.get("regionname")
#     region_type = request.args.get("regiontype")
    
#     if not region_name or not region_type:
#         return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

#     try:
#         with connection.cursor() as cursor:
#             # SQL query to join tables and filter based on regionname and regiontype
#             query = '''
#             SELECT 
#                 rc.regionid, 
#                 rc.regionname, 
#                 rc.regiontype, 
#                 mhi.date, 
#                 mhi.value 
#             FROM 
#                 public."Regions_cleaned" rc
#             JOIN 
#                 public.mhi_processed_by_metro_cleaned mhi
#             ON 
#                 rc.regionid = mhi.regionid
#             WHERE 
#                 rc.regionname = %s AND rc.regiontype = %s
#             ORDER BY 
#                 mhi.date ASC
#             '''
#             # Execute query with parameters
#             cursor.execute(query, (region_name, region_type))
#             rows = cursor.fetchall()

#             # Get column names
#             col_names = [desc[0] for desc in cursor.description]

#             # Format results as a list of dictionaries
#             result = [dict(zip(col_names, row)) for row in rows]
#             return {"data": result}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500


# @app.route("/get_mhi_data", methods=["GET"])
# def get_mhi_data():
#     # Get query parameters
#     region_name = request.args.get("regionname")
#     region_type = request.args.get("regiontype")
    
#     # Check for missing parameters
#     if not region_name or not region_type:
#         return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

#     try:
#         with connection.cursor() as cursor:
#             # SQL query to join tables and filter based on regionname and regiontype
#             query = '''
#             SELECT 
#                 rc.regionid, 
#                 rc.regionname, 
#                 rc.regiontype, 
#                 mhi.date, 
#                 mhi.value 
#             FROM 
#                 public."Regions_cleaned" rc
#             JOIN 
#                 public.mhi_processed_by_metro_cleaned mhi
#             ON 
#                 rc.regionid = mhi.regionid
#             WHERE 
#                 rc.regionname = %s AND rc.regiontype = %s
#             ORDER BY 
#                 mhi.date ASC
#             '''
#             # Execute query with parameters
#             cursor.execute(query, (region_name, region_type))
#             rows = cursor.fetchall()

#             # Get column names
#             col_names = [desc[0] for desc in cursor.description]

#             # Format results as a list of dictionaries
#             result = [dict(zip(col_names, row)) for row in rows]
#             return {"data": result}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500


@app.route("/get_localities_zori", methods=["GET"])
def get_states_zori():
    locality_type = request.args.get('type')
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = "zori_processed_by_zori_{}_cleaned".format(locality_type)

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            query = f'''
                SELECT DISTINCT regionname, statename
                FROM {table_name} zori
                JOIN "Regions_cleaned" rc ON zori.regionid = rc.regionid
                WHERE regiontype = %s
                ORDER BY regionname ASC
                LIMIT %s OFFSET %s
            '''
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
            total_count = cursor.fetchone()[0]

            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_localities_zhvf", methods=["GET"])
def get_states_zhvf():
    locality_type = request.args.get('type')
    page = int(request.args.get("page", 1))  # Default to page 1
    limit = int(request.args.get("limit", 10))  # Default to 10 records per page
    offset = (page - 1) * limit  # Calculate OFFSET

    table_name = "zhvf_by_zhvf_{}_cleaned".format(locality_type)

    if locality_type == "metro":
        locality_type = "msa"

    try:
        with connection.cursor() as cursor:
            query = f'''
                SELECT DISTINCT regionname, statename
                FROM {table_name} zhvf
                JOIN "Regions_cleaned" rc ON zhvf.regionid = rc.regionid
                WHERE regiontype = %s
                ORDER BY regionname ASC
                LIMIT %s OFFSET %s
            '''
            cursor.execute(query, (locality_type, limit, offset))
            rows = cursor.fetchall()

            cursor.execute(f'SELECT COUNT(DISTINCT regionid) FROM {table_name}')
            total_count = cursor.fetchone()[0]

            response = {
                "options": [{"regionname": row[0], "state": row[1]} for row in rows],
                "totalPages": (total_count + limit - 1) // limit  # Calculate total pages
            }
            return response
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_mhi", methods=["GET"])
def get_mhi():
    locality_type = request.args.get('type')
    locality_name = request.args.get('name')

    valid_locality_types = ['state', 'metro']
    if locality_type not in valid_locality_types:
        return {"error": "Invalid locality type"}, 400

    if locality_type == 'metro':
        locality_type = 'msa'

    try:
        with connection.cursor() as cursor:
            if locality_type == 'metro':
                query = f'''
                    SELECT rc.regionname, date, value AS mhi
                    FROM mhi_processed_by_metro_cleaned mhi
                    JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
                    WHERE regionname = %s
                    ORDER BY date ASC
                '''
                cursor.execute(query, (locality_name,))
            elif locality_type == 'state':
                query = f'''
                    SELECT statename, date, AVG(CAST(value AS float)) AS mhi
                    FROM mhi_processed_by_metro_cleaned mhi
                    JOIN "Regions_cleaned" rc ON mhi.regionid = rc.regionid
                    WHERE statename = %s
                    GROUP BY statename, date
                    ORDER BY date ASC
                '''
                cursor.execute(query, (locality_name,))

            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(col_names, row)) for row in rows]

            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_forecast_data", methods=["GET"])
def get_forecast_data():
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")

    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            query = '''
                SELECT rc.regionid, rc.regionname, rc.regiontype, fl.date, fl.value
                FROM public."Regions_cleaned" rc
                JOIN public.forsalelistings_processed_by_metro_cleaned fl
                ON rc.regionid = fl.regionid
                WHERE rc.regionname = %s AND rc.regiontype = %s
                ORDER BY fl.date ASC
            '''
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(col_names, row)) for row in rows]

            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_newconsales_data", methods=["GET"])
def get_newconsales_data():
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")

    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            query = '''
                SELECT rc.regionid, rc.regionname, rc.regiontype, nc.date, nc.value
                FROM public."Regions_cleaned" rc
                JOIN public.newconsales_processed_by_metro_cleaned nc
                ON rc.regionid = nc.regionid
                WHERE rc.regionname = %s AND rc.regiontype = %s
                ORDER BY nc.date ASC
            '''
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(col_names, row)) for row in rows]

            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_newconsales_data", methods=["GET"])
def get_newconsales_data():
    # Get query parameters
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")
    
    # Check for missing parameters
    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            # SQL query to join tables and filter based on regionname and regiontype
            query = '''
            SELECT 
                rc.regionid, 
                rc.regionname, 
                rc.regiontype, 
                nc.date, 
                nc.value 
            FROM 
                public."Regions_cleaned" rc
            JOIN 
                public.newconsales_processed_by_metro_cleaned nc
            ON 
                rc.regionid = nc.regionid
            WHERE 
                rc.regionname = %s AND rc.regiontype = %s
            ORDER BY 
                nc.date ASC
            '''
            # Execute query with parameters
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()

            # Get column names
            col_names = [desc[0] for desc in cursor.description]

            # Format results as a list of dictionaries
            result = [dict(zip(col_names, row)) for row in rows]
            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    


@app.route("/get_forecast_data", methods=["GET"])
def get_forecast_data():
    # Get query parameters
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")
    
    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            # SQL query to join tables and filter based on regionname and regiontype
            query = '''
            SELECT 
                rc.regionid, 
                rc.regionname, 
                rc.regiontype, 
                fl.date, 
                fl.value 
            FROM 
                public."Regions_cleaned" rc
            JOIN 
                public.forsalelistings_processed_by_metro_cleaned fl
            ON 
                rc.regionid = fl.regionid
            WHERE 
                rc.regionname = %s AND rc.regiontype = %s
            ORDER BY 
                fl.date ASC
            '''
            # Execute query with parameters
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()

            # Get column names
            col_names = [desc[0] for desc in cursor.description]

            # Format results as a list of dictionaries
            result = [dict(zip(col_names, row)) for row in rows]
            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    


# @app.get("/get_mhi_data")
# def get_mhi_data():
#     # Get query parameters
#     region_name = request.args.get("regionname")
#     region_type = request.args.get("regiontype")
    
#     if not region_name or not region_type:
#         return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

#     try:
#         with connection.cursor() as cursor:
#             # SQL query to join tables and filter based on regionname and regiontype
#             query = '''
#             SELECT 
#                 rc.regionid, 
#                 rc.regionname, 
#                 rc.regiontype, 
#                 mhi.date, 
#                 mhi.value 
#             FROM 
#                 public."Regions_cleaned" rc
#             JOIN 
#                 public.mhi_processed_by_metro_cleaned mhi
#             ON 
#                 rc.regionid = mhi.regionid
#             WHERE 
#                 rc.regionname = %s AND rc.regiontype = %s
#             ORDER BY 
#                 mhi.date ASC
#             '''
#             # Execute query with parameters
#             cursor.execute(query, (region_name, region_type))
#             rows = cursor.fetchall()

#             # Get column names
#             col_names = [desc[0] for desc in cursor.description]

#             # Format results as a list of dictionaries
#             result = [dict(zip(col_names, row)) for row in rows]
#             return {"data": result}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500


@app.route("/get_mhi_data", methods=["GET"])
def get_mhi_data():
    # Get query parameters
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")
    
    # Check for missing parameters
    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            # SQL query to join tables and filter based on regionname and regiontype
            query = '''
            SELECT 
                rc.regionid, 
                rc.regionname, 
                rc.regiontype, 
                mhi.date, 
                mhi.value 
            FROM 
                public."Regions_cleaned" rc
            JOIN 
                public.mhi_processed_by_metro_cleaned mhi
            ON 
                rc.regionid = mhi.regionid
            WHERE 
                rc.regionname = %s AND rc.regiontype = %s
            ORDER BY 
                mhi.date ASC
            '''
            # Execute query with parameters
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()

            # Get column names
            col_names = [desc[0] for desc in cursor.description]

            # Format results as a list of dictionaries
            result = [dict(zip(col_names, row)) for row in rows]
            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/get_newconsales_data", methods=["GET"])
def get_newconsales_data():
    # Get query parameters
    region_name = request.args.get("regionname")
    region_type = request.args.get("regiontype")
    
    # Check for missing parameters
    if not region_name or not region_type:
        return {"error": "Missing required query parameters: 'regionname' and 'regiontype'"}, 400

    try:
        with connection.cursor() as cursor:
            # SQL query to join tables and filter based on regionname and regiontype
            query = '''
            SELECT 
                rc.regionid, 
                rc.regionname, 
                rc.regiontype, 
                nc.date, 
                nc.value 
            FROM 
                public."Regions_cleaned" rc
            JOIN 
                public.newconsales_processed_by_metro_cleaned nc
            ON 
                rc.regionid = nc.regionid
            WHERE 
                rc.regionname = %s AND rc.regiontype = %s
            ORDER BY 
                nc.date ASC
            '''
            # Execute query with parameters
            cursor.execute(query, (region_name, region_type))
            rows = cursor.fetchall()

            # Get column names
            col_names = [desc[0] for desc in cursor.description]

            # Format results as a list of dictionaries
            result = [dict(zip(col_names, row)) for row in rows]
            return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500



