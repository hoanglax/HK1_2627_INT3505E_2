from flask import Flask
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp

app = Flask(__name__)

app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
