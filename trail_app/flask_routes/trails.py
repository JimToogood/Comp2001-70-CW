from flask import Blueprint, jsonify, request
from flasgger import swag_from
from database import get_connection
from auth import require_auth


blueprint = Blueprint("trails", __name__, url_prefix="/trails")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:trail_id>", methods=["GET"])
@require_auth
@swag_from("docs/get_trail.yml")
def get_trail(trail_id=None):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run get command
        if trail_id == None:
            cursor.execute("EXEC CW2.Get_Trails")
        else:
            cursor.execute("EXEC CW2.Get_Trail_By_ID @trail_id = ?", trail_id)

        # Convert output to json
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return (jsonify(results), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        if "Trail does not exist" in str(error):
            return (jsonify({"error": "Trail does not exist"}), 404)    # 404 = Not Found status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("", methods=["POST"])
@require_auth
@swag_from("docs/create_trail.yml")
def create_trail():
    required_inputs = [
        "trail_name",
        "distance",
        "elevation_gain",
        "estimated_time",
        "route_type",
        "difficulty",
        "location_id"
    ]

    # Get given inputs from user
    data = request.get_json()

    # Check for any missing requirements
    missing_inputs = []
    for input in required_inputs:
        if input not in data:
            missing_inputs.append(input)
    
    if missing_inputs != []:
        # Output error json with missing requirements specified
        return (jsonify({"error": f"Missing requirement(s) = {', '.join(missing_inputs)}"}), 400)   # 400 = Bad Request status code

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run insert command
        cursor.execute("""
            EXEC CW2.Insert_Trail
                @trail_name = ?,
                @distance = ?,
                @elevation_gain = ?,
                @estimated_time = ?,
                @route_type = ?,
                @difficulty = ?,
                @location_id = ?
            """, (
                data["trail_name"],
                data["distance"],
                data["elevation_gain"],
                data["estimated_time"],
                data["route_type"],
                data["difficulty"],
                data["location_id"]
        ))

        # Commit changes to database
        conn.commit()
        return (jsonify({"message": "Trail inserted successfully"}), 201)   # 201 = Created status code
    
    except Exception as error:
        # Output error as json
        if "Location does not exist" in str(error):
            return (jsonify({"error": "Location does not exist"}), 404)     # 404 = Not Found status code
        elif "Trail with that name already exists" in str(error):
            return (jsonify({"error": "Trail with that name already exists"}), 409)     # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


# PATCH is used instead of PUT so that only values that are to be changed have to be provided
@blueprint.route("/<int:trail_id>", methods=["PATCH"])
@require_auth
@swag_from("docs/update_trail.yml")
def update_trail(trail_id):
    # Get given inputs from user
    data = request.get_json()

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run update command
        cursor.execute("""
            EXEC CW2.Update_Trail
                @trail_id = ?,
                @trail_name = ?,
                @distance = ?,
                @elevation_gain = ?,
                @estimated_time = ?,
                @route_type = ?,
                @difficulty = ?,
                @location_id = ?
            """,
                # data.get() is used over data[] so that if the value is not provided, NULL is used instead of producing an error
                trail_id,
                data.get("trail_name"),
                data.get("distance"),
                data.get("elevation_gain"),
                data.get("estimated_time"),
                data.get("route_type"),
                data.get("difficulty"),
                data.get("location_id")
        )
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Trail {trail_id} updated successfully"}), 200)    # 200 = OK status code

    except Exception as error:
        # Output error as json
        if "Trail does not exist" in str(error):
            return (jsonify({"error": "Trail does not exist"}), 404)    # 404 = Not Found status code
        elif "Location does not exist" in str(error):
            return (jsonify({"error": "Location does not exist"}), 404)     # 404 = Not Found status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:trail_id>", methods=["DELETE"])
@require_auth
@swag_from("docs/delete_trail.yml")
def delete_trail(trail_id):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run delete command
        cursor.execute("EXEC CW2.Delete_Trail @trail_id = ?", trail_id)
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Trail {trail_id} deleted successfully"}), 200)    # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        if "Trail does not exist" in str(error):
            return (jsonify({"error": "Trail does not exist"}), 404)    # 404 = Not Found status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()
