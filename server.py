import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import webbrowser
from threading import Timer

app = Flask(__name__)
CORS(app)

# DYNAMIC DATASET MATRIX (Organized by City -> Role -> Experience)
DUMMY_JOBS = [
    # ─── BANGALORE HUB ───────────────────────────────────────────────────────
    {
        "title": "AI Trainee Engineer", "company": "TechNova Solutions", "location": "Bangalore",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "LinkedIn", "salary": "₹6-8 LPA",
        "skills": ["Python", "Data Structures", "NLP Basics"]
    },
    {
        "title": "Junior Data Analyst", "company": "FinMetrics Corp", "location": "Bangalore",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "Naukri.com", "salary": "₹4.5-6 LPA",
        "skills": ["SQL", "Excel", "PowerBI"]
    },
    {
        "title": "Gen AI Systems Engineer", "company": "NexaGen Intelligence", "location": "Bangalore",
        "experience_tier": "1-3", "experience": "1-3 years", "source": "LinkedIn", "salary": "₹12-16 LPA",
        "skills": ["LangChain", "LLMs", "Vector DBs", "Python"]
    },
    {
        "title": "Senior Data Scientist", "company": "Alpha Core Labs", "location": "Bangalore",
        "experience_tier": "3+", "experience": "4+ years", "source": "Naukri.com", "salary": "₹22-30 LPA",
        "skills": ["Machine Learning", "LLMOps", "Distributed Systems"]
    },

    # ─── HYDERABAD HUB ───────────────────────────────────────────────────────
    {
        "title": "Associate AI Engineer", "company": "NeuralLabs", "location": "Hyderabad",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "Internshala", "salary": "₹5.5-7.5 LPA",
        "skills": ["Python", "TensorFlow", "Math Foundations"]
    },
    {
        "title": "Data Analyst Trainee", "company": "Prism Analytics", "location": "Hyderabad",
        "experience_tier": "0-1", "experience": "Fresher", "source": "Naukri.com", "salary": "₹4-5.5 LPA",
        "skills": ["SQL", "Excel", "Tableau"]
    },
    {
        "title": "AI Engineer (Computer Vision)", "company": "CyberMind Systems", "location": "Hyderabad",
        "experience_tier": "1-3", "experience": "1-3 years", "source": "Naukri.com", "salary": "₹11-15 LPA",
        "skills": ["PyTorch", "Computer Vision", "Transformers"]
    },
    {
        "title": "Lead Data Scientist", "company": "Prism Financial", "location": "Hyderabad",
        "experience_tier": "3+", "experience": "3-5 years", "source": "LinkedIn", "salary": "₹20-26 LPA",
        "skills": ["Predictive Modeling", "Spark", "Python"]
    },

    # ─── MUMBAI HUB ──────────────────────────────────────────────────────────
    {
        "title": "Junior Data Analyst", "company": "Bombay Capital Corp", "location": "Mumbai",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "Naukri.com", "salary": "₹5-6.5 LPA",
        "skills": ["SQL", "Excel", "PowerBI"]
    },
    {
        "title": "AI Engineer Intern", "company": "Bay AI Tech", "location": "Mumbai",
        "experience_tier": "0-1", "experience": "Fresher", "source": "Internshala", "salary": "₹4-6 LPA",
        "skills": ["Python", "Machine Learning Basics"]
    },
    {
        "title": "Data Scientist", "company": "Alpha Risk Analytics", "location": "Mumbai",
        "experience_tier": "1-3", "experience": "2+ years", "source": "LinkedIn", "salary": "₹13-17 LPA",
        "skills": ["Python", "Machine Learning", "Scikit-Learn"]
    },
    {
        "title": "VP Data Science & Analytics", "company": "Jiomart Digital", "location": "Mumbai",
        "experience_tier": "3+", "experience": "5+ years", "source": "LinkedIn", "salary": "₹30-40 LPA",
        "skills": ["Executive Strategy", "Big Data Architecture", "Cloud Ops"]
    },

    # ─── DELHI HUB ───────────────────────────────────────────────────────────
    {
        "title": "Junior Data Scientist", "company": "Delhi Analytics Hub", "location": "Delhi",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "Naukri.com", "salary": "₹5-7 LPA",
        "skills": ["Python", "Scikit-Learn", "Pandas"]
    },
    {
        "title": "Data Analyst Intern", "company": "Capital Insights", "location": "Delhi",
        "experience_tier": "0-1", "experience": "Fresher", "source": "Internshala", "salary": "₹3.5-5 LPA",
        "skills": ["SQL", "Python", "Tableau"]
    },
    {
        "title": "Data Analyst (Mid-Level)", "company": "Vedic Commerce", "location": "Delhi",
        "experience_tier": "1-3", "experience": "2+ years", "source": "Naukri.com", "salary": "₹8-11 LPA",
        "skills": ["Advanced SQL", "Python", "PowerBI"]
    },
    {
        "title": "Senior Gen AI Specialist", "company": "Delta AI Corp", "location": "Delhi",
        "experience_tier": "3+", "experience": "3+ years", "source": "LinkedIn", "salary": "₹22-28 LPA",
        "skills": ["RAG Architecture", "Agentic Workflows", "API Tuning"]
    },

    # ─── CHENNAI HUB ─────────────────────────────────────────────────────────
    {
        "title": "Junior AI Engineer", "company": "Coromandel Tech", "location": "Chennai",
        "experience_tier": "0-1", "experience": "0-1 years", "source": "LinkedIn", "salary": "₹5-7 LPA",
        "skills": ["Python", "OpenCV", "C++ Foundations"]
    },
    {
        "title": "Data Analyst Graduate Trainee", "company": "Madras Analytics Group", "location": "Chennai",
        "experience_tier": "0-1", "experience": "Fresher", "source": "Naukri.com", "salary": "₹4.5-6 LPA",
        "skills": ["SQL", "Excel", "Data Wrangling"]
    },
    {
        "title": "Data Scientist (NLP Focused)", "company": "DeepSouth AI", "location": "Chennai",
        "experience_tier": "1-3", "experience": "2+ years", "source": "LinkedIn", "salary": "₹12-15 LPA",
        "skills": ["Python", "Transformers", "BERT", "SQL"]
    },
    {
        "title": "Principal AI Research Scientist", "company": "SaaS Titan Corp", "location": "Chennai",
        "experience_tier": "3+", "experience": "5+ years", "source": "Naukri.com", "salary": "₹26-34 LPA",
        "skills": ["Deep Learning", "PyTorch", "Academic Research Publishing"]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_jobs():
    role_query = request.form.get('role', '').strip().lower()
    location_query = request.form.get('location', '').strip().lower()
    exp_tier_query = request.form.get('experience', '').strip()
    
    resume_file = request.files.get('resume')
    if not resume_file or resume_file.filename == '':
        return jsonify({"status": "error", "message": "Please upload your resume to match skills properly."}), 400

    # Forgiving Whitelist Check: Ensures search has matching job domain keywords
    allowed_keywords = ["ai", "data", "engineer", "scientist", "analyst", "genai"]
    matched_role = any(keyword in role_query for keyword in allowed_keywords)
    
    if not role_query or not matched_role:
        return jsonify({
            "status": "error",
            "message": f'No job match matrices setup for "{request.form.get("role")}". Try searching for: Data Scientist, Data Analyst, AI Engineer, or Gen AI Engineer.'
        }), 404

    filtered_results = []
    role_words = [w.strip() for w in role_query.replace('-', ' ').split() if w.strip()]
    
    for job in DUMMY_JOBS:
        job_title = job['title'].lower().strip()
        job_location = job['location'].lower().strip()
        job_exp_tier = job['experience_tier'].strip()
        
        # 1. Broad keyword match against title
        role_matches = any(word in job_title for word in role_words) if role_words else False
        
        # 2. Case-insensitive substring location match
        location_matches = (location_query in job_location) or (job_location in location_query)
        
        # 3. Match against dropdown selection index string
        exp_matches = (job_exp_tier == exp_tier_query)
        
        if role_matches and location_matches and exp_matches:
            base_score = 87
            if exp_tier_query == "1-3": base_score = 93
            if exp_tier_query == "3+": base_score = 98
            
            job_copy = job.copy()
            job_copy['match_score'] = base_score
            filtered_results.append(job_copy)

    filtered_results = sorted(filtered_results, key=lambda x: x['match_score'], reverse=True)
    return jsonify({"status": "success", "data": filtered_results})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    Timer(1.5, open_browser).start()
    app.run(debug=True, port=5000)