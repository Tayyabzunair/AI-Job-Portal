import re, os, PyPDF2, json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart_job_portal_key_2026_secure" # Secret key updated for session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# --- Gemini API Configuration ---
GENAI_API_KEY = "xxxxxxxxxxxxxxxxxx" 
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # Fixed model version for stability

# ==================== MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20)) 

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    skills = db.Column(db.Text)
    salary = db.Column(db.String(50))
    requirements = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    benefits = db.Column(db.Text) # Added benefits column
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))
    deadline = db.Column(db.String(50))

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    skills = db.Column(db.Text)
    match_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="Pending")
    file_name = db.Column(db.String(100))
    job = db.relationship('Job', backref='applications')

# ==================== HELPERS ====================

def extract_details_llm(text):
    prompt = f"Return ONLY a valid JSON: {{'name': '...', 'email': '...', 'phone': '...', 'skills': '...'}}. Text: {text[:3500]}"
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except:
        return {"name": "Not Found", "email": "Not Found", "phone": "Not Found", "skills": ""}

def calculate_score(candidate_skills, required_skills):
    if not required_skills: return 0
    c_set = set([s.strip().lower() for s in str(candidate_skills).split(',')])
    r_set = set([s.strip().lower() for s in str(required_skills).split(',')])
    match = c_set.intersection(r_set)
    return round((len(match) / len(r_set)) * 100) if r_set else 0

# ==================== ROUTES ====================

@app.route('/')
def home(): 
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user = User(name=request.form.get('name'), email=request.form.get('email'), 
                        password=request.form.get('password'), role=request.form.get('role'))
        db.session.add(new_user); db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session.permanent = True # Session becomes permanent
        session['user_id'], session['role'], session['name'] = user.id, user.role, user.name
        if user.role == 'Owner':
            return redirect(url_for('view_candidates'))
        return redirect(url_for('candidate_dashboard'))
    return "Login Failed. <a href='/'>Try Again</a>"

@app.route('/logout')
def logout(): 
    session.clear()
    return redirect(url_for('home'))

# --- Owner Side ---
@app.route('/candidates')
def view_candidates():
    if session.get('role') != 'Owner': return redirect(url_for('home'))
    candidates = Resume.query.order_by(Resume.match_score.desc()).all()
    jobs = Job.query.all()
    return render_template('dashboard.html', candidates=candidates, jobs=jobs, total=len(candidates), name=session.get('name'))

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if session.get('role') != 'Owner': return redirect(url_for('home'))
    if request.method == 'POST':
        new_job = Job(
            title=request.form.get('title'), experience=request.form.get('experience'),
            skills=request.form.get('skills'), salary=request.form.get('salary'),
            requirements=request.form.get('requirements'), responsibilities=request.form.get('responsibilities'),
            benefits=request.form.get('benefits'), # Benefits handling added
            location=request.form.get('location'), job_type=request.form.get('job_type'), 
            deadline=request.form.get('deadline')
        )
        db.session.add(new_job); db.session.commit()
        return redirect(url_for('view_candidates'))
    return render_template('post_job.html', is_edit=False)

@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    if session.get('role') != 'Owner': return redirect(url_for('home'))
    job = Job.query.get_or_404(id)
    if request.method == 'POST':
        job.title = request.form.get('title'); job.location = request.form.get('location')
        job.salary = request.form.get('salary'); job.deadline = request.form.get('deadline')
        job.skills = request.form.get('skills'); job.requirements = request.form.get('requirements')
        job.responsibilities = request.form.get('responsibilities'); job.job_type = request.form.get('job_type')
        job.benefits = request.form.get('benefits')
        db.session.commit()
        return redirect(url_for('view_candidates'))
    return render_template('post_job.html', job=job, is_edit=True)

@app.route('/delete_job/<int:id>')
def delete_job(id):
    if session.get('role') != 'Owner': return redirect(url_for('home'))
    job = Job.query.get(id)
    if job: db.session.delete(job); db.session.commit()
    return redirect(url_for('view_candidates'))

@app.route('/update_status/<int:id>/<string:new_status>')
def update_status(id, new_status):
    if session.get('role') != 'Owner': return redirect(url_for('home'))
    res = Resume.query.get(id)
    if res: res.status = new_status; db.session.commit()
    return redirect(url_for('view_candidates'))

@app.route('/view_resume/<filename>')
def view_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Candidate Side ---
@app.route('/candidate_dashboard')
def candidate_dashboard():
    if session.get('role') != 'Candidate': return redirect(url_for('home'))
    jobs = Job.query.all()
    apps = Resume.query.filter_by(user_id=session['user_id']).all()
    applied_ids = {a.job_id: a.status for a in apps}
    return render_template('candidate_dashboard.html', jobs=jobs, applied_jobs=applied_ids, name=session.get('name'))

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if session.get('role') != 'Candidate': return redirect(url_for('home'))
    selected_job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename != '':
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            text = ""
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            details = extract_details_llm(text)
            return render_template('confirm_application.html', details=details, job=selected_job, filename=file.filename)
    return render_template('upload.html', job=selected_job)

@app.route('/finalize_application', methods=['POST'])
def finalize_application():
    if 'user_id' not in session: return redirect(url_for('home'))
    new_res = Resume(user_id=session['user_id'], job_id=request.form.get('job_id'),
                     name=request.form.get('name'), email=request.form.get('email'),
                     phone=request.form.get('phone'), skills=request.form.get('skills'),
                     match_score=calculate_score(request.form.get('skills'), request.form.get('job_skills')),
                     file_name=request.form.get('filename'))
    db.session.add(new_res); db.session.commit()
    return redirect(url_for('candidate_dashboard'))

# --- Chatbot ---
# app.py snippet
@app.route('/chatbot_query', methods=['POST'])
def chatbot_query():
    user_msg = request.json.get('message', '')
    # ... baki data gathering logic ...
    
    # Proper formatting instruction
    prompt = f"""
    Context: {data_context}
    User Query: {user_msg}
    
    Instructions:
    1. Respond as a professional Recruitment Manager.
    2. Use Markdown formatting: Use ## for Headings and * for bullet points.
    3. If listing candidates, give a proper summary in points.
    4. Speak naturally in Roman Urdu or English.
    """
    # ... baki Gemini call logic ...

@app.route('/chat')
def chat_page(): 
    if 'user_id' not in session: return redirect(url_for('home'))
    return render_template('chatbot.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'): os.makedirs('uploads')
    with app.app_context(): db.create_all()

    app.run(debug=True)
