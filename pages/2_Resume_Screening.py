import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("📄 Resume Screening")

# Load Dataset
df = pd.read_excel("Resume.xlsx")

# Get Categories
categories = sorted(df["Category"].unique())

selected_category = st.selectbox(
    "Select Job Category",
    categories
)

job_description = st.text_area(
    "Enter Job Description",
    height=250,
    placeholder="Paste the job description here..."
)

st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stExpander {
    background-color: #1C1F26;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Text Cleaning Function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Skill List
skills = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",
    "flask",
    "django",
    "git",
    "docker",
    "aws",
    "excel",
    "power bi",
    "tableau",
    "communication",
    "data analysis"
]

# Extract Skills
def extract_skills(text):
    text = text.lower()
    return [skill for skill in skills if skill in text]

# Analyze Button
if st.button("🔍 Analyze Resumes"):

    if job_description.strip() == "":
        st.warning("Please enter a Job Description.")
        st.stop()

    # Filter Category
    filtered_df = df[df["Category"] == selected_category].copy()

    if filtered_df.empty:
        st.error("No resumes found in this category.")
        st.stop()

    # Clean Resume Text
    filtered_df["Cleaned_Resume"] = filtered_df["Resume_str"].apply(clean_text)

    # Clean Job Description
    job_description = clean_text(job_description)

    # TF-IDF
    documents = [job_description] + filtered_df["Cleaned_Resume"].tolist()

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    ).flatten()

    filtered_df["Score"] = scores * 100

    # Skills
    job_skills = extract_skills(job_description)

    filtered_df["Skills"] = filtered_df["Cleaned_Resume"].apply(extract_skills)

    filtered_df["Missing Skills"] = filtered_df["Skills"].apply(
        lambda x: list(set(job_skills) - set(x))
    )

    # Ranking
    ranked = filtered_df.sort_values(
        by="Score",
        ascending=False
    )
    st.success("Analysis Completed ✅")

    st.subheader("🏆 Top Ranked Candidates")

    top10 = ranked.head(10)

    for index, row in top10.iterrows():

        with st.expander(f"Candidate ID: {row['ID']} | Score: {row['Score']:.2f}%"):

            st.write(f"**Category:** {row['Category']}")
            st.write(f"**Similarity Score:** {row['Score']:.2f}%")

            st.write("### ✅ Skills Found")

            if row["Skills"]:
                for skill in row["Skills"]:
                    st.write(f"- {skill}")
            else:
                st.write("No matching skills found.")

            st.write("### ❌ Missing Skills")

            if row["Missing Skills"]:
                for skill in row["Missing Skills"]:
                    st.write(f"- {skill}")
            else:
                st.success("No missing skills 🎉")
