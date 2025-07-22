from flask import Flask
from flask_routes import comments, locations, trails, users


# Create app
app = Flask(__name__)

# Import blueprints from python files in "flask_routes"
app.register_blueprint(comments.blueprint)
app.register_blueprint(locations.blueprint)
app.register_blueprint(trails.blueprint)
app.register_blueprint(users.blueprint)

# Handler for default domain
@app.route("/")
def index():
    return "Flask is successfully running!"

# Run app
if __name__ == "__main__":
    app.run(debug=True)
