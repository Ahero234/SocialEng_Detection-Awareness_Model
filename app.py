from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise database
# db = SQLAlchemy(app)

# Blueprints
from backend.detect_model.detect import detect_blueprint 
from backend.awareness.quiz import quiz_blueprint
from backend.awareness.education import education_blueprint

app.register_blueprint(detect_blueprint)
app.register_blueprint(quiz_blueprint)
app.register_blueprint(education_blueprint)

# View home page 
@app.route('/')
def index():
    return render_template('main/index.html')

if __name__ == "__main__":
    app.run(debug=True)