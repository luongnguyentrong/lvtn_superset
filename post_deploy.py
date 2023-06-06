from dotenv import load_dotenv
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_db_conn(db_name: str):
    # Connect to PostgreSQL
    conn = psycopg2.connect(dsn=os.getenv("POSTGRES_DSN") + "/" + db_name) 

    conn.autocommit = True
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);

    return conn

def main():
    # Load local env variables
    load_dotenv()

    # Check if the folder name is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Please provide a unit name as a command-line argument.")
        sys.exit(1)

    try:
        # Get the folder name from the command-line argument
        unit_name = sys.argv[1]

        # create a connection to metadata database
        db_conn = create_db_conn("metadata")

        # update superset_status of <unit_name> to success
        with db_conn.cursor() as cursor:
            # Update the superset_status

            update_query = f"UPDATE units SET superset_status = 'success' WHERE name = '{unit_name}'"
            cursor.execute(update_query)

        # close db conn
        db_conn.close()

        print("Post deploy success!")

    except Exception as e:
        print("Provision failed: ", e)

main()