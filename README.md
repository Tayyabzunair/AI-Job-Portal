---

# 🚀 AI-Powered Smart Job Portal

An advanced, automated recruitment ecosystem that leverages **Gemini 1.5 Flash AI** to transform traditional hiring into a seamless, data-driven experience. Built with a premium **Glassmorphism UI**, this platform automates resume parsing, candidate ranking, and talent analytics.

## 🌟 Key Features

### 🤖 Intelligent Resume Parsing

* **Automated PDF Extraction**: Extracts raw text from uploaded PDF resumes using `PyPDF2`.
* **AI Data Structuring**: Uses Gemini AI to parse unstructured text into structured JSON (Name, Email, Phone, Skills).
* **Auto-Fill Verification**: Candidates can review and edit AI-extracted data before final submission.

### 📊 Advanced Recruitment Tools

* **AI Match Scoring**: Automatically calculates a percentage match score between candidate skills and job requirements.
* **Interactive AI Assistant**: An integrated chatbot that answers queries about applicant stats and hiring trends using natural language.
* **Pipeline Management**: Owner dashboard to track application status from 'Pending' to 'Hired' or 'Rejected'.

### 🎨 Premium User Experience

* **Glassmorphism UI**: A futuristic design system using semi-transparent layers and blurred backgrounds.
* **Background Animations**: Smooth, animated mesh gradients for a modern tech vibe.
* **Responsive Design**: Fully optimized for both desktop and mobile recruitment.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLAlchemy (SQLite)
* **AI Engine**: Google Gemini 1.5 Flash
* **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
* **PDF Processing**: PyPDF2

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Google Gemini API Key

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/smart-job-portal.git
cd smart-job-portal

```


2. **Install dependencies**:
```bash
pip install flask flask_sqlalchemy google-generativeai pypdf2

```


3. **Configure API Key**:
Open `app.py` and replace the placeholder with your Gemini API key:
```python
GENAI_API_KEY = "YOUR_API_KEY_HERE"

```


4. **Initialize & Run**:
```bash
python app.py

```


The app will automatically create the database and start at `http://127.0.0.1:5000`.

## 📂 Project Structure

```text
SMART_JOB_PORTAL/
├── instance/           # Database storage
├── static/             # Assets and CSS
├── templates/          # Modern UI HTML files
├── uploads/            # Stored PDF resumes
└── app.py              # Main application logic

```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new AI features or UI improvements, feel free to open an issue or submit a pull request.

---

**Developed by Muhammad Tayyab Zunair**
*Student at Khawaja Fareed University*

---
