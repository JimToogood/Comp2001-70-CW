from flask import Blueprint, jsonify, request
from database import get_connection


blueprint = Blueprint("comments", __name__, url_prefix="/comments")

@blueprint.route("", methods=["GET"])
@blueprint.route("/<int:comment_id>", methods=["GET"])
def get_comment(comment_id=None):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run get command
        if comment_id == None:
            cursor.execute("EXEC CW2.Get_Comments")
        else:
            cursor.execute("EXEC CW2.Get_Comment_By_ID @comment_id = ?", comment_id)
        
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
def create_comment():
    required_inputs = [
        "trail_id",
        "user_id",
        "content"
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
            EXEC CW2.Insert_Comment
                @trail_id = ?,
                @user_id = ?,
                @content = ?
            """, (
                data["trail_id"],
                data["user_id"],
                data["content"]
        ))

        # Commit changes to database
        conn.commit()
        return (jsonify({"message": "Comment inserted successfully"}), 201)     # 201 = Created status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


# PUT is used instead of PATCH as there is only one variable that can be changed
@blueprint.route("/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    # Get given inputs from user
    data = request.get_json()

    # Check for missing requirement
    if "content" not in data:
        # Output error json with missing requirement specified
        return (jsonify({"error": "Missing requirement = content"}), 500)

    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run update command
        cursor.execute("""
            EXEC CW2.Update_Comment
                @comment_id = ?,
                @content = ?
            """,
                comment_id,
                data["content"]
        )
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Comment {comment_id} updated successfully"}), 200)    # 200 = OK status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()


@blueprint.route("/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    try:
        # Open connection to database
        conn = get_connection()
        cursor = conn.cursor()

        # Run delete command
        cursor.execute("EXEC CW2.Delete_Comment @comment_id = ?", comment_id)
        
        # Commit changes to database
        conn.commit()
        return (jsonify({"message": f"Comment {comment_id} deleted successfully"}), 200)    # 200 = OK status code
    
    except Exception as error:
        # Output error as json with error code
        return (jsonify({"error": str(error)}), 500)

    finally:
        # Close connection to database
        conn.close()
