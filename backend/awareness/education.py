from flask import Flask, render_template, Blueprint

education_blueprint = Blueprint("education", __name__, template_folder="templates")

@education_blueprint.route('/education')
def education_page():
    return render_template('education/education.html')
