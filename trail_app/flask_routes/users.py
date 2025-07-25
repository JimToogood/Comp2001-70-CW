from flask import Blueprint, jsonify, request
from flasgger import swag_from
from database import get_connection


blueprint = Blueprint("users", __name__, url_prefix="/users")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:user_id>", methods=["GET"])
@swag_from("docs/get_user.yml")
def get_user(user_id=None):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run get command
        if user_id == None:
            cursor.execute("EXEC CW2.Get_Users")
        else:
            cursor.execute("EXEC CW2.Get_User_By_ID @user_id = ?", user_id)
        
        # Convert output to json
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return (jsonify(results), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("", methods=["POST"])
@swag_from("docs/create_user.yml")
def create_user():
    required_inputs = [
        "email",
        "role"
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
            EXEC CW2.Insert_User
                @email = ?,
                @role = ?
            """, (
                data["email"],
                data["role"]
        ))

        # Commit changes to database
        conn.commit()
        return (jsonify({"message": "User inserted successfully"}), 201)    # 201 = Created status code
    
    except Exception as error:
        # Output error as json
        if "Email already exists" in str(error):
            return (jsonify({"error": "Email already exists"}), 409)    # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


# PATCH is used instead of PUT so that only values that are to be changed have to be provided
@blueprint.route("/<int:user_id>", methods=["PATCH"])
@swag_from("docs/update_user.yml")
def update_user(user_id):
    # Get given inputs from user
    data = request.get_json()

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run update command
        cursor.execute("""
            EXEC CW2.Update_User
                @user_id = ?,
                @email = ?,
                @role = ?
            """,
                # data.get() is used over data[] so that if the value is not provided, NULL is used instead of producing an error
                user_id,
                data.get("email"),
                data.get("role")
        )
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"User {user_id} updated successfully"}), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        if "User does not exist" in str(error):
            return (jsonify({"error": "User does not exist"}), 404)     # 404 = Not Found status code
        elif "Email already exists" in str(error):
            return (jsonify({"error": "Email already exists"}), 409)    # 409 = Conflict status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:user_id>", methods=["DELETE"])
@swag_from("docs/delete_user.yml")
def delete_user(user_id):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run delete command
        cursor.execute("EXEC CW2.Delete_User @user_id = ?", user_id)
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"User {user_id} deleted successfully"}), 200)  # 200 = OK status code
    
    except Exception as error:
        # Output error as json
        if "User does not exist" in str(error):
            return (jsonify({"error": "User does not exist"}), 404)     # 404 = Not Found status code
        else:
            return (jsonify({"error": str(error)}), 500)    # 500 = Internal Server Error status code

    finally:
        # Close connection to database
        conn.close()
