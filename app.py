# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise database
# db = SQLAlchemy(app)

# BLUEPRINTS
from backend.detect_model.detect import detect_blueprint 

app.register_blueprint(detect_blueprint)

# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')

if __name__ == "__main__":
    app.run(debug=True)