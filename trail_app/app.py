from flask import Flask
from flasgger import Swagger
from flask_routes import comments, locations, trails, users


# Create app
app = Flask(__name__)
swagger = Swagger(app)

# Import blueprints from python files in "flask_routes"
app.register_blueprint(comments.blueprint)
app.register_blueprint(locations.blueprint)
app.register_blueprint(trails.blueprint)
app.register_blueprint(users.blueprint)

# Handler for default domain
@app.route("/")
def index():
    return "Add /apidocs to the URL to see Swagger UI"

# Run app
if __name__ == "__main__":
    app.run(debug=True)
