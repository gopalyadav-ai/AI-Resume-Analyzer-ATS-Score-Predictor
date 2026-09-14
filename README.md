# AI Resume Analyzer & ATS Score Predictor

An AI-powered Resume Analyzer that evaluates a resume against a job description and generates an ATS compatibility score with practical AI-based suggestions.

The project combines Natural Language Processing (NLP), semantic similarity, skill matching, and Gemini AI to help identify how well a resume matches a target job description.

## Features

* Upload a resume in PDF format
* Extract resume text using PDF parsing
* Preprocess and normalize resume and job description text
* Extract technical skills from resume and job description
* Identify matched and missing skills
* Calculate semantic similarity between resume and job description
* Calculate resume completeness
* Generate an overall ATS compatibility score
* Generate AI-powered resume improvement suggestions using Gemini
* Interactive Streamlit web interface

## Technologies Used

* Python
* Streamlit
* NLP
* Sentence Transformers
* Scikit-learn
* PDFPlumber
* Google Gemini API
* Pandas / NumPy concepts
* Git & GitHub

## Project Workflow

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Text Preprocessing
    ↓
Skill Extraction
    ↓
Resume vs Job Description Comparison
    ↓
Skill Matching + Semantic Similarity
    ↓
Resume Completeness Analysis
    ↓
ATS Score Calculation
    ↓
Gemini AI Suggestions
    ↓
Streamlit Results
```

## ATS Scoring

The project calculates the ATS compatibility score using multiple components:

| Component           |  Weight |
| ------------------- | ------: |
| Semantic Similarity |      30 |
| Skill Match         |      40 |
| Education           |      10 |
| Experience          |      10 |
| Resume Completeness |      10 |
| **Total**           | **100** |

### 1. Semantic Similarity

The project uses the `all-MiniLM-L6-v2` Sentence Transformer model to convert the resume and job description into embeddings.

Cosine similarity is then used to measure how closely the resume content matches the job description.

### 2. Skill Match

Technical skills are extracted from both the resume and job description.

The analyzer identifies:

* Matched skills
* Missing skills
* Skill match percentage

### 3. Resume Completeness

The analyzer checks for important resume sections such as:

* About
* Technical Skills
* Education
* Projects
* Experience
* Certifications

### 4. Education and Experience

The system checks the resume for relevant education and experience keywords and includes them in the overall ATS compatibility score.

## Gemini AI Integration

Google Gemini is used to generate personalized resume feedback based on the calculated ATS results.

The AI suggestions can include:

* Resume strengths
* Missing skills
* Resume weaknesses
* Suggestions to improve ATS compatibility
* Final recommendation

The Gemini API key is loaded through an environment variable and is **not stored in the source code**.

```text
GEMINI_API_KEY
```

Do not upload your real API key to GitHub.

## Installation

Clone the repository:

```bash
git clone https://github.com/gopalyadav-ai/AI-Resume-Analyzer-ATS-Score-Predictor.git
cd AI-Resume-Analyzer-ATS-Score-Predictor
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Gemini API Key Setup

The application uses the `GEMINI_API_KEY` environment variable.

### Windows Command Prompt

```cmd
set GEMINI_API_KEY=YOUR_API_KEY
```

Then run the application in the same Command Prompt window.

Do not replace `YOUR_API_KEY` in this README with your actual key.

## Run the Application

Start Streamlit using:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Upload your resume as a PDF.
2. Paste the target job description.
3. Click **Analyze Resume**.
4. The application processes the resume.
5. Review the ATS compatibility score.
6. Check matched and missing skills.
7. Review resume completeness.
8. Read the AI-generated improvement suggestions.

## Example Result

The application provides:

* ATS Score
* Resume Match Percentage
* Skill Match Percentage
* Matched Skills
* Missing Skills
* Resume Completeness
* AI Resume Suggestions

Example:

```text
ATS Score: 83.49 / 100
Resume Match: 57.10%
Skill Match: 90.91%

Matched Skills:
Python, Machine Learning, Deep Learning, NLP,
TensorFlow, Keras, AWS, LangChain

Missing Skills:
Azure
```

The exact score depends on the resume and job description provided by the user.

## Project Structure

```text
AI-Resume-Analyzer-ATS-Score-Predictor/
│
├── AI Resume Analyzer .ipynb
├── app.py
├── utils.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Files Description

### `AI Resume Analyzer .ipynb`

Contains the complete project development process, experiments, NLP processing, semantic similarity analysis, ATS scoring logic, and testing.

### `app.py`

Contains the Streamlit application used to interact with the Resume Analyzer.

### `utils.py`

Contains the core processing functions including:

* PDF text extraction
* Text preprocessing
* Skill extraction
* Skill matching
* Semantic similarity
* Resume completeness calculation
* ATS score calculation
* Gemini AI suggestions

### `requirements.txt`

Contains the Python dependencies required to run the application.

### `.gitignore`

Prevents temporary files, Python cache files, environment files, and other unnecessary files from being uploaded to GitHub.

## Limitations

* PDF text extraction quality depends on the structure and formatting of the resume.
* Skill extraction is based on a predefined technical skill list.
* ATS scoring is based on this project's own scoring methodology and should not be considered the exact score used by a commercial ATS.
* Gemini suggestions require a valid Gemini API key.
* The analyzer is designed primarily for text-based PDF resumes.

## Future Improvements

* Add support for DOCX resumes
* Improve skill extraction using advanced NLP models
* Add keyword context and experience-level matching
* Improve semantic matching using domain-specific embeddings
* Add job-specific resume recommendations
* Add downloadable analysis reports
* Add resume section quality analysis
* Deploy the application to a cloud platform

## Author

**Gopal Yadav**