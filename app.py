from flask import Flask, render_template, request, send_file
from speech_input import get_audio
from analyzer import analyze_answer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

# ✅ NEW: environment switch
USE_MIC = os.environ.get("USE_MIC", "true") == "true"

roles = {

    "software":[
        "Tell me about yourself",
        "Explain a programming project you built",
        "What programming languages do you know?",
        "How do you debug a program?",
        "Why should we hire you?"
    ],

    "data":[
        "Tell me about yourself",
        "What tools do you use for data analysis?",
        "Explain a data analysis project",
        "What is data cleaning?",
        "How do you handle missing data?"
    ],

    "marketing":[
        "Tell me about yourself",
        "How would you promote a new product?",
        "Explain a marketing campaign you like",
        "What social media strategies work best?",
        "How do you measure campaign success?"
    ]

}

questions = []
scores = []
question_index = 0


@app.route("/preparation")
def preparation():

    qa = [
        {"question":"Tell me about yourself","answer":"Start with your background, current studies, and key skills."},
        {"question":"What are your strengths?","answer":"Mention strengths with examples."},
        {"question":"What are your weaknesses?","answer":"Mention weakness and improvement."},
        {"question":"Why should we hire you?","answer":"Explain why you're suitable."},
        {"question":"Why do you want to work here?","answer":"Align your goals with company."},
        {"question":"Describe a challenge you faced","answer":"Use STAR method."},
        {"question":"Where do you see yourself in 5 years?","answer":"Show growth and ambition."},
        {"question":"Tell me about teamwork experience","answer":"Explain your role in team."},
        {"question":"How do you handle pressure?","answer":"Give real example."},
        {"question":"What motivates you?","answer":"Talk about growth and learning."}
    ]

    return render_template("preparation.html", qa=qa)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/generate_resume", methods=["POST"])
def generate_resume():

    name = request.form.get("name")
    skills = request.form.get("skills")
    education = request.form.get("education")

    return render_template(
        "resume.html",
        name=name,
        skills=skills,
        education=education,
        generated=True
    )


@app.route("/download_resume", methods=["POST"])
def download_resume():

    name = request.form.get("name")
    skills = request.form.get("skills")
    education = request.form.get("education")

    file_path = "resume.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(f"<b>{name}</b>", styles["Title"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"<b>Education:</b> {education}", styles["Normal"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"<b>Skills:</b> {skills}", styles["Normal"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph("<b>Projects:</b> AI Interview System", styles["Normal"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph("<b>Objective:</b> Motivated individual seeking opportunities.", styles["Normal"]))

    doc.build(content)

    return send_file(file_path, as_attachment=True)


@app.route("/role/<role>")
def select_role(role):

    global questions, scores, question_index

    if role not in roles:
        return render_template("home.html")

    questions = roles[role]
    scores = []
    question_index = 0

    return render_template("start.html", role=role)


@app.route("/question")
def question_page():

    global question_index

    if not questions:
        return render_template("home.html")

    progress = int((question_index)/len(questions)*100)

    return render_template(
        "interview.html",
        question=questions[question_index],
        q_number=question_index+1,
        total=len(questions),
        progress=progress,
        USE_MIC=USE_MIC   # ✅ pass to HTML
    )


@app.route("/record", methods=["GET", "POST"])
def record():

    global question_index, scores

    if not questions:
        return render_template("home.html")

    # ✅ SWITCH INPUT
    if USE_MIC:
        answer = get_audio()
    else:
        answer = request.form.get("answer")

    score, feedback = analyze_answer(answer)

    scores.append(score)
    question_index += 1

    progress = int((question_index)/len(questions)*100)

    if question_index >= len(questions):

        final_score = round(sum(scores)/len(scores), 2)

        return render_template(
            "result.html",
            final_score=final_score
        )

    return render_template(
        "interview.html",
        question=questions[question_index],
        answer=answer,
        feedback=feedback,
        score=score,
        q_number=question_index+1,
        total=len(questions),
        progress=progress,
        USE_MIC=USE_MIC   # ✅ pass again
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)