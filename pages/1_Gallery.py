import streamlit as st
import pandas as pd
import os
from PIL import Image

# Hardcoded mapping
id_to_name = {
    55: "living_things", 56: "actions", 57: "types_of_people", 58: "concepts",
    59: "types_of_places", 60: "food_and_drink", 61: "objects", 62: "fiction",
    63: "famous places", 64: "brands", 65: "countries", 66: "landmarks",
    67: "sports", 68: "society_and_culture", 69: "science_and_tech",
    70: "artists", 71: "video_games", 72: "movies"
}

# Load data
df = pd.read_csv("deception_dashboard/labled_drawings.csv")
df["category_name"] = df["category_id"].map(id_to_name)

# Title
st.title("Drawings Deceptive to AI")

# Sidebar filters
st.sidebar.header("Filters")

# Category filter
all_categories = sorted(df["category_name"].unique())
selected_category = st.sidebar.selectbox("Choose Category", ["All"] + all_categories)
filtered_df = df[df["category_name"] == selected_category].copy()

# Filter by category
if selected_category != "All":
    filtered_df = df[df["category_name"] == selected_category].copy()
else:
    filtered_df = df.copy()

# Technique filter (only options present in selected category)
technique_options = set()
filtered_df["technique_used"].dropna().apply(
    lambda x: [technique_options.add(t.strip()) for t in x.split(",")]
)
selected_technique = st.sidebar.selectbox("Filter by Technique", ["All"] + sorted(technique_options))

# Apply technique filter
if selected_technique != "All":
    filtered_df = filtered_df[filtered_df["technique_used"].str.contains(selected_technique)]

# Prioritize rows with notes
filtered_df["has_notes"] = filtered_df["notes"].notnull() & (filtered_df["notes"].str.strip() != "")
filtered_df = filtered_df.sort_values(by="has_notes", ascending=False)

# Show grid of images
st.subheader(f" {len(filtered_df)} Drawings in {selected_category}")

cols = st.columns(3)
for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 3]  # loop over 3 columns
    with col:
        category_folder = str(row["category_id"])
        image_path = os.path.join("deception_dashboard/images", category_folder, row["image_path"])
        if os.path.exists(image_path):
            st.image(Image.open(image_path), caption=row["ground_truth"], use_container_width=True)
            st.markdown(f"`{row['technique_used']}`")
            
            # Show notes only if they exist and are not 'nan' or blank
            notes = str(row["notes"]).strip().lower()
            if notes and notes != "nan":
                st.markdown(f"Notes: *{row['notes'].strip()}*")
        else:
            st.warning(f"Missing: {image_path}")
