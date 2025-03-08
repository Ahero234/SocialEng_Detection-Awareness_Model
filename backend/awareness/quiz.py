'''@quiz_blueprint.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answers = {q: request.form.get(q) for q in range(len(quiz_data))}
        session['answers'] = user_answers
        return render_template('results.html', quiz_data=quiz_data, user_answers=user_answers)
    return render_template('quiz.html', quiz_data=quiz_data)

@quiz_blueprint.route('/results')
def results():
    user_answers = session.get('answers', {})
    return render_template('results.html', quiz_data=quiz_data, user_answers=user_answers)'''

from flask import Flask, render_template, request, session, Blueprint, redirect, url_for
import random

quiz_blueprint = Blueprint("quiz", __name__, template_folder="templates")

quiz_data = [
    {
        "question": "You receive an email claiming to be from your bank, asking you to click on a link to verify your account details due to a security breach. What should you do?",
        "options": {
            "a": "Click on the link and provide the requested information",
            "b": "Forward the email to your friends for advice",
            "c": "Forward the email to your personal email account so you can open it at home",
            "d": "Call your bank to verify the authenticity of the email"
        },
        "correct": "d"
    },
    {
        "question": "While using an ATM, you notice an unusual device attached to the card slot. What should you do?",
        "options": {
            "a": "Ignore it and proceed with your transaction",
            "b": "Report it to the bank staff immediately",
            "c": "Take a picture and post it on social media for awareness",
            "d": "Attempt to remove the device yourself"
        },
        "correct": "b"
    }
    # Add more questions here
]

total_questions = len(quiz_data)  # Number of questions to be asked before showing results

@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    # Initialise session variables if they don't exist
    if "score" not in session:
        session["score"] = 0
    if "question_count" not in session:
        session["question_count"] = 0
    if "asked_questions" not in session:
        session["asked_questions"] = []

    # Check if the quiz is complete
    if session["question_count"] >= total_questions:
        return redirect(url_for('quiz.results_page'))

    # Handle form submission
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')

        # Check the answered question
        for question in quiz_data:
            if question["question"] == question_text:
                if question["correct"] == user_answer:
                    session["score"] += 1  #  Add 1 point if correct
                session["question_count"] += 1
                break

        # Redirect to the next question or results page
        if session["question_count"] >= total_questions:
            return redirect(url_for('quiz.results_page'))
        else:
            return redirect(url_for('quiz.quiz_page'))

    # Select a new question randomly that has not been asked already
    remaining_questions = [q for q in quiz_data if q["question"] not in session["asked_questions"]]
    if not remaining_questions:  # Reset if all questions are used
        session["asked_questions"] = []
        remaining_questions = quiz_data

    question = random.choice(remaining_questions)
    session["asked_questions"].append(question["question"])

    return render_template('quiz/quiz.html', question=question, question_number=session["question_count"] + 1, total_questions=total_questions)

@quiz_blueprint.route('/results')
def results_page():
    score = session.get("score", 0)
    total = session.get("question_count", 0)

    # Reset session data for a new quiz attempt
    session.pop("score", None)
    session.pop("question_count", None)
    session.pop("asked_questions", None)

    return render_template('quiz/results.html', score=score, total=total)