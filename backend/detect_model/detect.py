from flask import Blueprint, request, render_template
import pickle

detect_blueprint = Blueprint("detect", __name__, template_folder="templates")

# Load phishing detection model
def load_model():
    model = None
    vectorizer = None

    try:
        with open("backend/model.pkl", "rb") as model_file:
            model = pickle.load(model_file)

        with open("backend/vectorizer.pkl", "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
    except Exception as e:
        print(f"Error loading model: {e}")

    return model, vectorizer

model, vectorizer = load_model()

# Ensure model is loaded correctly
if model is None or vectorizer is None:
    print("Error: Model or vectorizer could not be loaded.")


@detect_blueprint.route("/detect", methods=["GET"])
def detect_form():
    return render_template("detect/detect.html", result=None)


@detect_blueprint.route('/detect', methods=['POST'])
def detect():
    try:
        message = request.form.get('email', '').strip()
        if not message:
            return render_template("detect/detect.html", prediction="Error: Email content is required")

        # Transform input and predict
        vect = vectorizer.transform([message]).toarray()
        prediction = model.predict(vect)[0]

        result = "Beware! This could potentially be a phishing email!" if prediction == 1 else "This email appears safe."
        return render_template('detect/detect.html', prediction=result)

    except Exception as e:
        return render_template("detect/detect.html", prediction=f"An error occurred: {str(e)}")