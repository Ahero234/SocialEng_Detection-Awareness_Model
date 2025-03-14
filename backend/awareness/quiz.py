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
        "correct": "d",
        "explanation": "Legitimate banks never ask for sensitive information via email. Always contact your bank directly through their official phone number or website."
    },
    {
        "question": "While using an ATM, you notice an unusual device attached to the card slot. What should you do?",
        "options": {
            "a": "Ignore it and proceed with your transaction",
            "b": "Report it to the bank staff immediately",
            "c": "Take a picture and post it on social media for awareness",
            "d": "Attempt to remove the device yourself"
        },
        "correct": "b",
        "explanation": "You must report suspicious devices to the bank to prevent fraud."
    },
    {
        "question": "Which of the following is a common sign of a phishing email?",
        "options": {
            "a": "A legitimate-looking sender address",
            "b": "Urgent or threatening language",
            "c": "A request for personal information",
            "d": "Both b) and c)"
        },
        "correct": "d",
        "explanation": "Phishing emails often use urgency and request personal information to trick users into providing credentials."
    },
    {
        "question": "Which of these links is most likely to be a phishing attempt?",
        "options": {
            "a": "https://paypal.com/login",
            "b": "https://secure-paypal.com/settings",
            "c": "https://amazon.com/order-history",
            "d": "https://www.amazon.com/account/settings"
        },
        "correct": "b",
        "explanation": "Attackers often create fake domains with slight modifications, such as 'secure-paypal.com', to appear legitimate."
    }, 
    {
        "question": "What is Pretexting?",
        "options": {
            "a": "A method where an attacker creates a fabricated scenario to obtain information",
            "b": "A method where an attacker uses a false promise to lure a victim into a trap to steal personal information",
            "c": "A form of phishing attack",
            "d": "A way of spoofing a website to steal login details"
        },
        "correct": "a",
        "explanation": "Pretexting involves fabricating a scenario to gain trust and extract sensitive information."
    },
    {
        "question": "What does HTTPS stand for?",
        "options": {
            "a": "High-Traffic Transfer Protocol Standard",
            "b": "Hyperlink Technology Protection System",
            "c": "HyperText Transfer Protocol Secure",
            "d": "HyperText Translation Privacy Security"
        },
        "correct": "c",
        "explanation": "HTTPS encrypts data between a user's browser and a website, ensuring secure communication."
    }, 
    {
        "question": "What is the main goal of a social engineering attack?",
        "options": {
            "a": "To spread malware to victims",
            "b": "To test an organization's security",
            "c": "To trick individuals into revealing confidential information",
            "d": "All of the above"
        },
        "correct": "c",
        "explanation": "Social engineering relies on manipulating individuals into providing sensitive information rather than hacking systems."
    }, 
    {
        "question": "You get an email about a refund from Amazon, but you don't recall making a purchase. What is the best response?",
        "options": {
            "a": "Click the link to verify your purchase history",
            "b": "Call the number in the email for customer support",
            "c": "Reply to the email asking for more details",
            "d": "Log in to your Amazon account directly (not via email links) to check"
        },
        "correct": "d",
        "explanation": "Scammers send fake refund emails to trick users into clicking malicious links. Always check directly on the official website."
    },
    {
        "question": "What is the best way to handle a suspicious email attachment?",
        "options": {
            "a": "Download it and scan it with antivirus software",
            "b": "Delete it immediately without opening",
            "c": "Open it in an isolated virtual machine",
            "d": "Both a) and c)"
        },
        "correct": "b",
        "explanation": "Opening suspicious attachments can lead to malware infections. It's safer to delete them without opening."
    }, 
    {
        "question": "What is a common sign of a spear-phishing attack?",
        "options": {
            "a": "A message referencing specific details about you that aren't public",
            "b": "A sender using an official company domain",
            "c": "A generic email greeting like 'Dear Valued Customer'",
            "d": "Both a) and c)"
        },
        "correct": "a",
        "explanation": "Spear-phishing attacks are highly targeted and use specific details about the victim to appear more convincing."
    },
    {
        "question": "Which of the following is an example of a quid pro quo attack?",
        "options": {
            "a": "A hacker installs malware through an infected USB drive",
            "b": "A scammer offers free software in exchange for login credentials",
            "c": "A cybercriminal sets up a fake login page",
            "d": "An attacker sends a phishing email with a fake link"
        },
        "correct": "b",
        "explanation": "Quid pro quo attacks offer a benefit (like free software) in exchange for confidential information."
    },
    {
        "question": "What is the best way attackers can use social media for social engineering?",
        "options": {
            "a": "By hacking into a company's website",
            "b": "By sending ransomware via private messages",
            "c": "By creating fake profiles to build trust and extract information",
            "d": "By installing spyware on user accounts automatically"
        },
        "correct": "c",
        "explanation": "Attackers use fake social media profiles to build trust and gather information from targets."
    },
    {
        "question": 'You receive an email from "admin@yourcompany-secure.com" asking you to update your login details. What is the biggest red flag?',
        "options": {
            "a": "The email creates a sense of urgency",
            "b": "The message contains technical jargon about security updates",
            "c": "The email is not signed by your IT department",
            "d": "The sender's address is slightly different from the official domain"
        },
        "correct": "d",
        "explanation": "Attackers often use similar-looking domains (e.g., 'yourcompany-secure.com' instead of 'yourcompany.com') to deceive users."
    }
]

total_questions = 10 # len(quiz_data)

@quiz_blueprint.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    if "score" not in session:
        session["score"] = 0
    if "question_count" not in session:
        session["question_count"] = 0
    if "feedback" not in session:
        session["feedback"] = []
    if "question_order" not in session or len(session["question_order"]) < total_questions:
        session["question_order"] = random.sample(quiz_data, total_questions)  # Shuffle unique questions

    # If quiz is complete, redirect to results page
    if session["question_count"] >= total_questions:
        return redirect(url_for('quiz.results_page'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')

        for question in session["question_order"]:
            if question["question"] == question_text:
                correct_answer = question["correct"]
                explanation = question["explanation"]

                session["feedback"].append({
                    "question": question_text,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "is_correct": user_answer == correct_answer,
                    "explanation": explanation
                })

                if user_answer == correct_answer:
                    session["score"] += 1
                session["question_count"] += 1
                break

        return redirect(url_for('quiz.quiz_page'))

    # Get the next question in order
    question = session["question_order"][session["question_count"]]

    return render_template('quiz/quiz.html', question=question, question_number=session["question_count"] + 1, total_questions=total_questions)

@quiz_blueprint.route('/results')
def results_page():
    score = session.get("score", 0)
    total = session.get("question_count", 0)
    feedback = session.get("feedback", [])

    # Reset session data for a new quiz attempt
    session.pop("score", None)
    session.pop("question_count", None)
    session.pop("feedback", None)
    session.pop("question_order", None)

    return render_template('quiz/results.html', score=score, total=total, feedback=feedback)