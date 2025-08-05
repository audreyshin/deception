import streamlit as st
import pandas as pd
import os
import plotly.express as px
from collections import Counter

# Hardcoded category ID to name mapping (from your screenshot)
id_to_name = {
    55: "living_things",
    56: "actions",
    57: "types_of_people",
    58: "concepts",
    59: "types_of_places",
    60: "food_and_drink",
    61: "objects",
    62: "fiction",
    63: "famous places",
    64: "brands",
    65: "countries",
    66: "landmarks",
    67: "sports",
    68: "society_and_culture",
    69: "science_and_tech",
    70: "artists",
    71: "video_games",
    72: "movies"
}

# Load labeled drawing data
df = pd.read_csv("labled_drawings.csv")
df["category_name"] = df["category_id"].map(id_to_name)

st.title("Technique Analytics")
st.markdown("Analyze how humans trick AI in sketch recognition using visual deception techniques.")


# --- Section: Full Technique Distribution ---
st.subheader(" Frequency of All Techniques")
all_technique_counts = Counter()
for techs in df["technique_used"].dropna():
    all_technique_counts.update([t.strip() for t in techs.split(",")])

dist_df = pd.DataFrame(all_technique_counts.items(), columns=["Technique", "Count"]).sort_values("Count", ascending=False)
st.plotly_chart(px.bar(dist_df, x="Technique", y="Count", title=""))



# --- Section: Heatmap of Techniques by Category ---


st.subheader("Frequency of Techniques by Category")

# Expand each technique entry into rows
expanded = df.dropna(subset=["technique_used"]).copy()
expanded["technique_used"] = expanded["technique_used"].str.split(",")
expanded = expanded.explode("technique_used")
expanded["technique_used"] = expanded["technique_used"].str.strip()

# Create a pivot table
pivot = pd.pivot_table(expanded, index="category_name", columns="technique_used", aggfunc="size", fill_value=0)

# Plot heatmap
fig = px.imshow(pivot, 
                labels=dict(x="Technique", y="Category", color="Count"),
                aspect="auto",
                title="")
st.plotly_chart(fig)

# --- Section: Most Common Technique(s) per Category ---
st.subheader("Most Used Technique per Category")
category_groups = df.groupby("category_name")["technique_used"]
most_common_per_category = []
for cat, tech_list in category_groups:
    counter = Counter()
    for tech_str in tech_list.dropna():
        counter.update([t.strip() for t in tech_str.split(",")])
    if counter:
        top_tech = counter.most_common(1)[0]
        most_common_per_category.append({"Category": cat, "Top Technique": top_tech[0], "Count": top_tech[1]})

cat_df = pd.DataFrame(most_common_per_category).sort_values("Count", ascending=False)
st.dataframe(cat_df)
