from flask import Blueprint, jsonify
from database import get_connection


blueprint = Blueprint("locations", __name__, url_prefix="/locations")

@blueprint.route("", methods=["GET"])
def get_locations():
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run get command
        cursor.execute("EXEC CW2.Get_Locations")
        
        # Convert output to json
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify(results)
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


# TODO: POST, PATCH, DELETE
