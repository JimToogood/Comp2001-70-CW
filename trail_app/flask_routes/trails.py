from flask import Blueprint, jsonify, request
from database import get_connection


blueprint = Blueprint("trails", __name__, url_prefix="/trails")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:trail_id>", methods=["GET"])
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

        return jsonify(results)
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("", methods=["POST"])
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
        return (jsonify({"error": f"Missing requirement(s) = {', '.join(missing_inputs)}"}), 500)

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
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


# PATCH is used instead of PUT so that only values that are to be changed have to be provided
@blueprint.route("/<int:trail_id>", methods=["PATCH"])
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
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:trail_id>", methods=["DELETE"])
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
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()
