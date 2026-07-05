import streamlit as st
import pandas as pd

st.title("👤 Candidate Details")

# Load dataset
df = pd.read_csv("Resume.xlsx")

# Select Category
categories = sorted(df["Category"].unique())

selected_category = st.selectbox(
    "Select Category",
    categories
)

# Filter data
filtered_df = df[df["Category"] == selected_category]

# Select Candidate ID
candidate_id = st.selectbox(
    "Select Candidate ID",
    filtered_df["ID"].tolist()
)

# Show details
candidate = filtered_df[filtered_df["ID"] == candidate_id].iloc[0]

st.subheader("📌 Candidate Information")

st.write(f"**ID:** {candidate['ID']}")
st.write(f"**Category:** {candidate['Category']}")

st.markdown("---")

st.subheader("📄 Resume Preview")

st.text(candidate["Resume_str"][:1000])

st.markdown("---")

st.info("👉 Go to Resume Screening page to see scores, skills, and ranking.")
