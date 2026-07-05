import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Resume Dataset
df = pd.read_csv("Resume.xlsx")

print("First 5 Rows:\n")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nDataset Shape:")
print(df.shape)
# -------------------------
#  Category  Selection 
# -------------------------
print("\nAvailable Categories:")
print(df["Category"].unique())

selected_category = input("\nEnter the category (Example: DATA SCIENCE): ").upper()

# -----------------------------------------
# Filter resumes based on selected category
# -----------------------------------------
filtered_df = df[df["Category"].str.upper() == selected_category]

if filtered_df.empty:
    print("No resumes found for this category.")
    exit()

print(f"\nTotal resumes found: {len(filtered_df)}")

# -----------------------
# Text Cleaning Function
# ----------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# --------------------
# Clean Resume Text
# -------------------
filtered_df["Cleaned_Resume"] = filtered_df["Resume_str"].apply(clean_text)

print("\nOriginal Resume:\n")
print(df["Resume_str"].iloc[0][:300])

print("\nCleaned Resume:\n")
print(df["Cleaned_Resume"].iloc[0][:300])

# --------------------------
# Read Job Description
# ---------------------------
with open("job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

job_description = clean_text(job_description)

# -----------------------------
# TF-IDF + Cosine Similarity
# -----------------------------

documents = [job_description] + filtered_df["Cleaned_Resume"].tolist()

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)
similarity_scores = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:]
).flatten()

filtered_df["Score"] = similarity_scores * 100

# -----------
# Skill List
# -----------

skills = [
    "python","sql","machine learning","deep learning","pandas","numpy","scikit-learn","tensorflow","keras","flask",
    "django","git","docker","aws","excel","power bi","tableau","communication","data analysis"
]
# ==========================
# Skill Extraction
# ==========================
def extract_skills(text):
    found = []
    text = text.lower()
    for skill in skills:
        if skill in text:
            found.append(skill)
    return found
job_skills = extract_skills(job_description)
print("\nJob Skills:")
print(job_skills)

filtered_df["Skills"] = df["Cleaned_Resume"].apply(extract_skills)

# ==========================
# Missing Skills
# ==========================
def missing_skills(candidate_skills, required_skills):
    return list(set(required_skills) - set(candidate_skills))
filtered_df["Skills"] = df["Cleaned_Resume"].apply(extract_skills)
["Missing Skills"] = df["Skills"].apply
(
    lambda x: missing_skills(x, job_skills)
)

# ==========================
# Rank Candidates
# ==========================
ranked_candidates = filtered_df.sort_values(
    by="Score",
    ascending=False
)

print("\nTop 5 Candidate Scores:\n")
print(
    ranked_candidates[
        ["ID", "Category", "Score"]
    ].head()
)

# ==========================
# Display Top 5 Candidates
# ==========================
top5 = ranked_candidates.head(5)
print("\nTop 5 Candidates Details\n")
for _, row in top5.iterrows():
    print("=" * 70)
    print(f"Candidate ID : {row['ID']}")
    print(f"Category     : {row['Category']}")
    print(f"Score        : {row['Score']:.2f}%")
    print("\nSkills Found:")
    print(row["Skills"])
    print("\nMissing Skills:")
    print(row["Missing Skills"])
    
    

print("\nProgram Executed Successfully.")
