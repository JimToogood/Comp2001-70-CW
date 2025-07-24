from flask import Blueprint, jsonify, request
from database import get_connection


blueprint = Blueprint("locations", __name__, url_prefix="/locations")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:location_id>", methods=["GET"])
def get_location(location_id=None):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run get command
        if location_id == None:
            cursor.execute("EXEC CW2.Get_Locations")
        else:
            cursor.execute("EXEC CW2.Get_Location_By_ID @location_id = ?", location_id)
        
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
def create_location():
    # Get given inputs from user
    data = request.get_json()

    # Check for missing requirement
    if "location_name" not in data:
        # Output error json with missing requirement specified
        return (jsonify({"error": "Missing requirement = location_name"}), 500)

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run insert command
        cursor.execute("""
            EXEC CW2.Insert_Location
                @location_name = ?
            """, (
                data["location_name"]
        ))

        # Commit changes to database
        conn.commit()
        return (jsonify({"message": "Location inserted successfully"}), 201)    # 201 = Created status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


# PUT is used instead of PATCH as there is only one variable that can be changed
@blueprint.route("/<int:location_id>", methods=["PUT"])
def update_location(location_id):
    # Get given inputs from user
    data = request.get_json()

    # Check for missing requirement
    if "location_name" not in data:
        # Output error json with missing requirement specified
        return (jsonify({"error": "Missing requirement = location_name"}), 500)

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run update command
        cursor.execute("""
            EXEC CW2.Update_Location
                @location_id = ?,
                @location_name = ?
            """,
                location_id,
                data["location_name"]
        )
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Location {location_id} updated successfully"}), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run delete command
        cursor.execute("EXEC CW2.Delete_Location @location_id = ?", location_id)
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Location {location_id} deleted successfully"}), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()
