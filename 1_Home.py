import streamlit as st

st.set_page_config(page_title="Resume AI System", layout="wide")

st.title("📄 AI Resume Screening System")

st.markdown("### 🚀 Smart Hiring with Machine Learning")

st.markdown("""
Welcome to the **AI-powered Resume Screening System**.

This system helps recruiters:
- Rank candidates automatically
- Match resumes with job descriptions
- Identify missing skills
- Save hiring time
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("📄 Resume Parsing")

with col2:
    st.success("🧠 AI Matching")

with col3:
    st.success("📊 Analytics Dashboard")