import re
import os
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


skills = [
    "python", "sql", "java", "c++",
    "machine learning", "machinelearning",
    "deep learning", "deeplearning",
    "nlp",
    "natural language processing", "naturallanguageprocessing",
    "transformers", "bert", "llm", "llms", "rag", "langchain",
    "computer vision", "computervision", "opencv", "cnn",
    "tensorflow", "keras", "scikit-learn", "scikitlearn",
    "pandas", "numpy", "matplotlib", "seaborn",
    "xgboost", "adaboost",
    "power bi", "powerbi", "tableau",
    "streamlit", "fastapi",
    "aws", "azure", "ibm watsonx", "watsonx",
    "mysql", "sqlite",
    "git", "github"
]


def extract_text_from_pdf(pdf_path):
    try:
        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    full_text += text + "\n"

        return full_text

    except Exception as e:
        print(f"Error: {e}")
        return None


def preprocess_text(text):
    text = text.lower()

    text = text.replace("machinelearning", "machine learning")
    text = text.replace("deeplearning", "deep learning")
    text = text.replace(
        "naturallanguageprocessing",
        "natural language processing"
    )
    text = text.replace("scikitlearn", "scikit-learn")
    text = text.replace("computervision", "computer vision")
    text = text.replace("promptengineering", "prompt engineering")
    text = text.replace("powerbi", "power bi")
    text = text.replace("githubcom", "github")

    text = " ".join(text.split())

    text = re.sub(r"[^\w\s\-]", "", text)

    return text


def extract_skills(text):
    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_skill_match_score(matched_skills, jd_skills):
    if not jd_skills:
        return 0.0

    return (len(matched_skills) / len(jd_skills)) * 100


def calculate_similarity(resume_text, jd_text):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd_text])

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    return float(similarity)


def calculate_completeness_score(text):
    section_keywords = {
        "About": ["about", "aboutme"],
        "Technical Skills": ["technical skills", "technicalskills"],
        "Education": ["education"],
        "Projects": ["projects"],
        "Experience": [
            "experience",
            "workexperience",
            "intern"
        ],
        "Certifications": [
            "certifications",
            "certification",
            "training"
        ]
    }

    count = 0

    for keywords in section_keywords.values():
        for keyword in keywords:
            if keyword in text:
                count += 1
                break

    score = (count / len(section_keywords)) * 10

    return score, count


def calculate_ats_score(
    similarity_score,
    skill_match_score,
    completeness_score,
    education_score=10,
    experience_score=10
):
    semantic_score = similarity_score * 30
    skills_score = (skill_match_score / 100) * 40

    total_score = (
        semantic_score +
        skills_score +
        education_score +
        experience_score +
        completeness_score
    )

    return total_score


def generate_ai_suggestions(
    matched_skills,
    missing_skills,
    ats_score,
    similarity_score,
    completeness_score
):
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return [
                "Gemini API key is not configured.",
                "Set the GEMINI_API_KEY environment variable to enable AI suggestions."
            ]

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the resume based on these ATS results.

ATS Score: {ats_score:.2f}/100

Resume Match Score: {similarity_score * 100:.2f}%

Skill Match Score: {len(matched_skills)} matched skills

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Resume Completeness Score:
{completeness_score}/10

Provide:

1. Resume Strengths
2. Missing Skills
3. Weaknesses
4. Suggestions to Improve ATS Score
5. Final Recommendation

Keep the response clear and practical.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return [response.text]

    except Exception as e:
        return [f"Gemini error: {e}"]