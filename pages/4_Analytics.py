import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Resume Intelligence Dashboard")

# Load dataset
df = pd.read_excel("Resume.xlsx")

# ---------------------------
# OVERVIEW SECTION
# ---------------------------
def shorten(role):
    mapping = {
        "INFORMATION TECHNOLOGY": "IT",
        "DATA SCIENCE": "DS",
        "ENGINEERING": "ENG",
        "FINANCE": "FIN",
        "HUMAN RESOURCES": "HR"
    }
    return mapping.get(role, role)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Resumes", df.shape[0])

with col2:
    st.metric("Job Categories", df["Category"].nunique())

with col3:
    st.metric("Most Common Role", df["Category"].value_counts().idxmax())
# ---------------------------
# TOP JOB CATEGORIES
# ---------------------------
st.subheader("🏆 Top Job Categories")

top_categories = df["Category"].value_counts().head(10)

st.dataframe(top_categories)


# ---------------------------
# CATEGORY DISTRIBUTION (%)
# ---------------------------
st.subheader("📊 Category Distribution (%)")

category_percent = df["Category"].value_counts(normalize=True).head(10) * 100

fig2, ax2 = plt.subplots(figsize=(5,4))
category_percent.plot(kind="bar", ax=ax2)
ax2.set_title("Category Share (%)")
ax2.set_ylabel("Percentage")
plt.xticks(rotation=75)


st.pyplot(fig2)

st.markdown("---")

# ---------------------------
# RESUME LENGTH INSIGHT
# ---------------------------
st.subheader("📄 Resume Complexity Analysis")

df["resume_length"] = df["Resume_str"].astype(str).apply(lambda x: len(x.split()))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Length", int(df["resume_length"].mean()))

with col2:
    st.metric("Shortest Resume", int(df["resume_length"].min()))

with col3:
    st.metric("Longest Resume", int(df["resume_length"].max()))

fig3, ax3 = plt.subplots()
ax3.hist(df["resume_length"], bins=25)
ax3.set_title("Resume Length Distribution")
ax3.set_xlabel("Word Count")
ax3.set_ylabel("Number of Resumes")

st.pyplot(fig3)

st.markdown("---")

# ---------------------------
# SKILL INSIGHTS (REAL VALUE PART)
# ---------------------------
st.subheader("🧠 Skill Insights from Resumes")

skills = [
    "python", "sql", "machine learning", "deep learning",
    "excel", "communication", "java", "aws", "docker",
    "data analysis", "power bi", "tableau"
]

df["text"] = df["Resume_str"].astype(str).str.lower()

skill_counts = {}

for skill in skills:
    skill_counts[skill] = df["text"].str.contains(skill).sum()

skill_df = pd.DataFrame(
    list(skill_counts.items()),
    columns=["Skill", "Count"]
).sort_values(by="Count", ascending=False)

fig4, ax4 = plt.subplots(figsize=(6, 3))
ax4.bar(skill_df["Skill"], skill_df["Count"])
ax4.set_title("Most Common Skills in Resumes")
ax4.set_ylabel("Frequency")
plt.xticks(rotation=75)

st.pyplot(fig4)

st.markdown("---")

# ---------------------------
# INSIGHTS (FINAL SECTION)
# ---------------------------
st.subheader("🔍 Key Insights for Recruiters")

most_common = df["Category"].value_counts().idxmax()
least_common = df["Category"].value_counts().idxmin()
top_skill = skill_df.iloc[0]["Skill"]

st.write(f"✔ Most common job role: **{most_common}**")
st.write(f"✔ Least common job role: **{least_common}**")
st.write(f"✔ Most frequently appearing skill: **{top_skill}**")

st.write("✔ This system helps recruiters understand candidate distribution and skill trends.")
