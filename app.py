import streamlit as st
from utils import (
    extract_text_from_pdf,
    preprocess_text,
    extract_skills,
    calculate_skill_match_score,
    calculate_similarity,
    calculate_completeness_score,
    calculate_ats_score,
    generate_ai_suggestions
)


st.set_page_config(
    page_title="AI Resume Analyzer & ATS Score Predictor",
    page_icon="📄",
    layout="wide"
)


st.title("AI Resume Analyzer & ATS Score Predictor")

st.write(
    "Upload your resume and paste a job description to analyze "
    "your ATS compatibility."
)


resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)


job_description = st.text_area(
    "Paste Job Description",
    height=250
)


if st.button("Analyze Resume"):

    if resume_file is None:
        st.warning("Please upload a resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        with st.spinner("Analyzing resume..."):

            # Save uploaded resume temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(resume_file.getbuffer())

            # Extract resume text
            resume_text = extract_text_from_pdf("temp_resume.pdf")

            if not resume_text:
                st.error("Could not extract text from the resume.")
                st.stop()

            # Preprocess text
            clean_resume = preprocess_text(resume_text)
            clean_jd = preprocess_text(job_description)

            # Extract skills
            resume_skills = extract_skills(clean_resume)
            jd_skills = extract_skills(clean_jd)

            # Matched and missing skills
            matched_skills = sorted(
                set(resume_skills) & set(jd_skills)
            )

            missing_skills = sorted(
                set(jd_skills) - set(resume_skills)
            )

            # Skill match
            skill_match_score = calculate_skill_match_score(
                matched_skills,
                jd_skills
            )

            # Semantic similarity
            similarity_score = calculate_similarity(
                clean_resume,
                clean_jd
            )

            # Completeness
            completeness_score, section_count = calculate_completeness_score(
                clean_resume
            )

            # Education
            education_keywords = [
                "bachelor",
                "b.sc",
                "btech",
                "b.tech",
                "computer science",
                "engineering",
                "master",
                "m.sc",
                "mtech"
            ]

            education_score = 0

            for keyword in education_keywords:
                if keyword in clean_resume:
                    education_score = 10
                    break

            # Experience
            experience_keywords = [
                "intern",
                "internship",
                "experience",
                "worked",
                "employee",
                "project"
            ]

            experience_score = 0

            for keyword in experience_keywords:
                if keyword in clean_resume:
                    experience_score = 10
                    break

            # ATS score
            ats_score = calculate_ats_score(
                similarity_score,
                skill_match_score,
                completeness_score,
                education_score,
                experience_score
            )

            # Gemini suggestions
            suggestions = generate_ai_suggestions(
                matched_skills,
                missing_skills,
                ats_score,
                similarity_score,
                completeness_score
            )


        st.success("Resume analysis completed!")


        st.subheader("ATS Score")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{ats_score:.2f}/100"
            )

        with col2:
            st.metric(
                "Resume Match",
                f"{similarity_score * 100:.2f}%"
            )

        with col3:
            st.metric(
                "Skill Match",
                f"{skill_match_score:.2f}%"
            )


        st.subheader("Strong / Matched Skills")

        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matching skills found.")


        st.subheader("Missing Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.write("No missing skills found.")


        st.subheader("Resume Completeness")

        st.write(
            f"{section_count} out of 6 important sections detected"
        )

        st.progress(
            min(section_count / 6, 1.0)
        )


        st.subheader("AI Resume Suggestions")

        for suggestion in suggestions:
            st.write(suggestion)