from flask import Blueprint, jsonify, request
from flasgger import swag_from
from database import get_connection
from auth import require_auth


blueprint = Blueprint("locations", __name__, url_prefix="/locations")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:location_id>", methods=["GET"])
@require_auth
@swag_from("docs/get_location.yml")
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

        return (jsonify(results), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        if "Location does not exist" in str(error):
            return (jsonify({"error": "Location does not exist"}), 404)     # 404 = Not Found status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("", methods=["POST"])
@require_auth
@swag_from("docs/create_location.yml")
def create_location():
    # Get given inputs from user
    data = request.get_json()

    # Check for missing requirement
    if "location_name" not in data:
        # Output error json with missing requirement specified
        return (jsonify({"error": "Missing requirement = location_name"}), 400)     # 400 = Bad Request status code

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
        # Output error as json
        if "Location with that name already exists" in str(error):
            return (jsonify({"error": "Location with that name already exists"}), 409)  # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


# PUT is used instead of PATCH as there is only one variable that can be changed
@blueprint.route("/<int:location_id>", methods=["PUT"])
@require_auth
@swag_from("docs/update_location.yml")
def update_location(location_id):
    # Get given inputs from user
    data = request.get_json()

    # Check for missing requirement
    if "location_name" not in data:
        # Output error json with missing requirement specified
        return (jsonify({"error": "Missing requirement = location_name"}), 400)     # 400 = Bad Request status code

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
        # Output error as json
        if "Location does not exist" in str(error):
            return (jsonify({"error": "Location does not exist"}), 404)     # 404 = Not Found status code
        elif "Location with that name already exists" in str(error):
            return (jsonify({"error": "Location with that name already exists"}), 409)  # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:location_id>", methods=["DELETE"])
@require_auth
@swag_from("docs/delete_location.yml")
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
        # Output error as json
        if "Location does not exist" in str(error):
            return (jsonify({"error": "Location does not exist"}), 404)     # 404 = Not Found status code
        elif "Cannot delete location as it is still referenced in CW2.Trails" in str(error):
            return (jsonify({"error": "Cannot delete location as it is still referenced in Trails"}), 409)  # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()
