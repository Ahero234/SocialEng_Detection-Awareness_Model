from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

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

# Error pages
@app.errorhandler(400)
def bad_request_error(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(403)
def forbidden_error(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(503)
def unavailable_service_error(error):
    return render_template("errors/503.html"), 503

if __name__ == "__main__":
    app.run(debug=True)