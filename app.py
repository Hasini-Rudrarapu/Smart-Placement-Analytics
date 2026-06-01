import streamlit as st
import pandas as pd
import plotly.express as px

from utils.pdf_reader import extract_text
from utils.skill_extractor import extract_skills
from utils.matcher import calculate_match

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --------------------
# HEADER
# --------------------
st.title("📄 Smart Resume Analyzer & Job Matcher")

st.markdown(
    """
    Analyze resumes, calculate ATS scores, and compare
    candidate skills with job descriptions.
    """
)

st.markdown("---")

# --------------------
# SIDEBAR
# --------------------
with st.sidebar:

    st.header("🚀 Project Features")

    st.success("Resume Parsing")
    st.success("Skill Extraction")
    st.success("ATS Score")
    st.success("Job Matching")
    st.success("Missing Skill Detection")
    st.success("Interactive Dashboard")

    st.markdown("---")

    st.info(
        """
        Built Using:
        - Python
        - Streamlit
        - NLP
        - PDF Parsing
        - Plotly
        """
    )

# --------------------
# INPUT SECTION
# --------------------
col1, col2 = st.columns(2)

with col1:

    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with col2:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=250
    )

# --------------------
# ANALYZE BUTTON
# --------------------
if st.button("🔍 Analyze Resume", use_container_width=True):

    if resume and job_description:

        with st.spinner("Analyzing Resume..."):

            # Extract Resume Text
            resume_text = extract_text(resume)

            # Extract Resume Skills
            skills = extract_skills(resume_text)

            # Calculate ATS Score
            score, matched, missing = calculate_match(
                resume_text,
                job_description
            )

        st.success("✅ Analysis Complete")

        # --------------------
        # ATS SCORE
        # --------------------
        st.subheader("📊 ATS Score")

        st.metric(
            "Resume Match %",
            f"{score}%"
        )

        st.progress(score / 100)

        if score >= 80:
            st.success("Excellent Match 🎉")

        elif score >= 60:
            st.info("Good Match 👍")

        else:
            st.warning("Needs Improvement ⚠️")

        st.markdown("---")

        # --------------------
        # EXTRACTED SKILLS
        # --------------------
        st.subheader("🛠 Extracted Skills")

        if skills:
            st.write(", ".join(skills))
        else:
            st.warning("No skills detected.")

        st.markdown("---")

        # --------------------
        # MATCHED & MISSING
        # --------------------
        col3, col4 = st.columns(2)

        with col3:

            st.subheader("✅ Matched Skills")

            if matched:
                for skill in matched:
                    st.success(skill)
            else:
                st.write("No matched skills.")

        with col4:

            st.subheader("❌ Missing Skills")

            if missing:
                for skill in missing:
                    st.error(skill)
            else:
                st.write("No missing skills.")

        st.markdown("---")

        # --------------------
        # PIE CHART
        # --------------------
        st.subheader("📈 Skill Match Analysis")

        chart_df = pd.DataFrame({
            "Category": ["Matched", "Missing"],
            "Count": [len(matched), len(missing)]
        })

        fig = px.pie(
            chart_df,
            values="Count",
            names="Category",
            title="Skill Match Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        # --------------------
        # SUMMARY
        # --------------------
        st.subheader("📋 Resume Summary")

        st.info(
            f"""
            Total Resume Skills: {len(skills)}

            Matched Skills: {len(matched)}

            Missing Skills: {len(missing)}

            ATS Score: {score}%
            """
        )

        st.markdown("---")

        # --------------------
        # RESUME PREVIEW
        # --------------------
        st.subheader("📄 Resume Text Preview")

        st.text_area(
            "Extracted Resume Text",
            resume_text[:3000],
            height=300
        )

    else:

        st.warning(
            "⚠ Please upload a resume and paste a job description."
        )