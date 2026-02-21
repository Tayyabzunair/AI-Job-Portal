
---

# 🚀 AI-Powered Smart Job Portal

An advanced, automated recruitment ecosystem that leverages **Google Gemini 1.5 Flash AI** to transform traditional hiring into a seamless, data-driven experience. Built with a premium **Glassmorphism UI**, this platform automates resume parsing, candidate ranking, and talent analytics.

## 🌟 Key Features

### 🤖 Intelligent Resume Parsing

* **Automated PDF Extraction**: Seamlessly extracts raw text from PDF resumes using `PyPDF2`.
* **AI Data Structuring**: Utilizes Gemini AI to parse unstructured text into precise JSON objects (Name, Email, Phone, Skills).
* **Auto-Fill Verification**: Candidates can review and edit AI-extracted information before final submission.

### 📊 Advanced Recruitment Tools

* **AI Match Scoring**: Automatically calculates a percentage match score by comparing candidate skills with job requirements.
* **Interactive AI Assistant**: An integrated chatbot that answers natural language queries about applicants and hiring trends.
* **Pipeline Management**: Specialized dashboard for Owners to track application statuses from 'Pending' to 'Hired'.

### 🎨 Premium User Experience

* **Glassmorphism UI**: A futuristic design system featuring semi-transparent layers and blurred backgrounds.
* **Background Animations**: Smooth, animated mesh gradients for a modern professional look.
* **Responsive Layout**: Fully optimized for desktop and mobile devices.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLAlchemy (SQLite)
* **AI Engine**: Google Gemini 1.5 Flash
* **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Bootstrap 5
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
Open `app.py` and replace the placeholder with your actual Gemini API key:
```python
GENAI_API_KEY = "YOUR_API_KEY_HERE"

```


4. **Initialize & Run**:
```bash
python app.py

```


The application will automatically initialize the database and start at `http://127.0.0.1:5000`.

## 📂 Project Structure

```text
SMART_JOB_PORTAL/
├── instance/           # Database storage
├── static/             # Assets and custom CSS
├── templates/          # Modern UI HTML files
├── uploads/            # Securely stored PDF resumes
└── app.py              # Central application logic

```

## 🛡️ Security Features

* **Role-Based Access Control**: Strict separation between Owner and Candidate functionalities.
* **Session Management**: Secure session handling to prevent unauthorized access.
* **File Validation**: Restricts uploads to PDF format only for system safety.

---

**Developed by Muhammad Tayyab Zunair**
*Student at Khawaja Fareed University*

---
