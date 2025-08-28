import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from itertools import combinations
import numpy as np

# === Load Live Google Sheet ===
csv_url = "https://docs.google.com/spreadsheets/d/1nGRDV27Wz3Xf3jfD_rlEsTeFebSAhFsnYYMMhbeO_jc/export?format=csv"
df = pd.read_csv(csv_url)

# === Map category ID to name ===
id_to_name = {
    55: "living_things", 56: "actions", 57: "types_of_people", 58: "concepts",
    59: "types_of_places", 60: "food_and_drink", 61: "objects", 62: "fiction",
    63: "famous places", 64: "brands", 65: "countries", 66: "landmarks",
    67: "sports", 68: "society_and_culture", 69: "science_and_tech",
    70: "artists", 71: "video_games", 72: "movies"
}
df["category_name"] = df["category_id"].map(id_to_name)

# === Filter out invalid test results ===
df = df[df["technique_used"].str.strip().str.lower() != "invalid test result"]

# === Page title and intro blurb ===
st.title("Technique Analytics Dashboard")
st.markdown("""
This dashboard explores how different drawing strategies are used to trick AI.
""")

# === Sidebar Filter ===
with st.sidebar:
    st.header("Filter Options")
    all_categories = sorted(df["category_name"].dropna().unique())
    selected_category = st.selectbox("Choose a Category", ["All"] + all_categories)

# === Apply Category Filter ===
filtered_df = df.copy() if selected_category == "All" else df[df["category_name"] == selected_category].copy()

if selected_category == "All":
    total_images = df.shape[0]
    analyzed_images = df["technique_used"].notna().sum()
    percent_done = (analyzed_images / 857) * 100

    st.markdown(
        f"<p style='font-size:16px;'>"
        f"<b>{analyzed_images}</b> out of <b>{857}</b> drawings have been labeled "
        f"({percent_done:.1f}%) so far."
        f"</p>",
        unsafe_allow_html=True
    )

else:
    category = selected_category
    total = df[df["category_name"] == category].shape[0]
    labeled = df[(df["category_name"] == category) & (df["technique_used"].notna())].shape[0]
    percent = (labeled / total) * 100 if total > 0 else 0

    st.markdown(
        f"<p style='font-size:16px;'>"
        f"<b>{labeled}</b> out of <b>{total}</b> drawings in <b>{category.replace('_', ' ').title()}</b> "
        f"have been labeled ({percent:.1f}%) so far."
        f"</p>",
        unsafe_allow_html=True
    )

st.subheader("Frequency of Techniques" + (f" in {selected_category}" if selected_category != "All" else ""))

view_mode = st.selectbox(
    "Choose Frequency View",
    ["Raw frequency (default)", "Category weighted frequency"]
)

if view_mode == "Raw frequency (default)":
    st.markdown(
        """
        <div style='font-size:15px; margin-bottom:10px;'>
        <b>Raw frequency</b> counts how often each technique appears across all drawings. 
        Categories with more drawings will naturally dominate the counts.
        </div>
        """,
        unsafe_allow_html=True
    )

    tech_counts = Counter()
    for techniques in filtered_df["technique_used"].dropna():
        tech_counts.update([t.strip() for t in techniques.split(",")])

    dist_df = pd.DataFrame(tech_counts.items(), columns=["Technique", "Count"]).sort_values("Count", ascending=False)

else:
    st.markdown(
        """
        <div style='font-size:15px; margin-bottom:10px;'>
        <b>Category weighted frequency</b> averages technique usage across all categories so that 
        no single category skews the result. Each category contributes equally.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Build category-weighted frequency
    df_exp = df.dropna(subset=["technique_used"]).copy()
    df_exp["technique_used"] = df_exp["technique_used"].str.split(",")
    df_exp = df_exp.explode("technique_used")
    df_exp["technique_used"] = df_exp["technique_used"].str.strip()

    cat_counts = df_exp.groupby("category_name")["technique_used"].value_counts(normalize=True).unstack(fill_value=0)
    dist_df = cat_counts.mean(axis=0).reset_index()
    dist_df.columns = ["Technique", "Count"]
    dist_df = dist_df.sort_values("Count", ascending=False)

# --- Show chart ---
if not dist_df.empty:
    fig = px.bar(
        dist_df,
        x="Technique",
        y="Count",
        labels={"Technique": "Technique", "Count": "Frequency"},
        color_discrete_sequence=["#e75480"]
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    # Dynamic summary
    top_technique = dist_df.iloc[0]
    view_label = "all drawings" if view_mode == "Raw frequency (default)" else "each category"
    context = selected_category if selected_category != "All" else "all categories"

    st.markdown(
        f"<p style='font-size:16px; margin-top: -10px;'>"
        f"The most used technique in <b>{context}</b> based on <b>{view_label}</b> is "
        f"<b>{top_technique['Technique']}</b>."
        f"</p>",
        unsafe_allow_html=True
    )


# === Section: Heatmap of Techniques by Category ===
if selected_category == "All":
    st.subheader("Heatmap")

    expanded = df.dropna(subset=["technique_used"]).copy()
    expanded["technique_used"] = expanded["technique_used"].str.split(",")
    expanded = expanded.explode("technique_used")
    expanded["technique_used"] = expanded["technique_used"].str.strip()

    pivot = pd.pivot_table(expanded, index="category_name", columns="technique_used", aggfunc="size", fill_value=0)

    fig = px.imshow(
        pivot,
        labels=dict(x="Technique", y="Category", color="Count"),
        color_continuous_scale="RdPu",
        width=1000,
        height=800
    )
    st.plotly_chart(fig)


def draw_cooccurrence_heatmap(df_subset, title):
    df_subset = df_subset.dropna(subset=["technique_used"]).copy()
    df_subset["technique_used"] = df_subset["technique_used"].str.split(",")
    df_subset["technique_used"] = df_subset["technique_used"].apply(lambda lst: [t.strip() for t in lst])

    all_techs = sorted({t for sublist in df_subset["technique_used"] for t in sublist})
    if len(all_techs) < 2:
        st.info("Not enough data to build a co-occurrence map.")
        return None

    co_matrix = pd.DataFrame(0, index=all_techs, columns=all_techs)

    for row in df_subset["technique_used"]:
        unique_techs = sorted(set(row))
        for t1, t2 in combinations(unique_techs, 2):
            co_matrix.loc[t1, t2] += 1
            co_matrix.loc[t2, t1] += 1

    fig = px.imshow(
        co_matrix,
        labels=dict(x="Technique", y="Technique", color="Co-occurrence"),
        title=title,
        color_continuous_scale="RdPu",
        width=1000,
        height=1000
    )
    st.plotly_chart(fig)

    return co_matrix 

if selected_category == "All":
    st.subheader("Technique Co-occurrence (All Categories)")
    co_matrix = draw_cooccurrence_heatmap(df, "")

else:
    st.subheader(f"Technique Co-occurrence for {selected_category}")
    co_matrix = draw_cooccurrence_heatmap(filtered_df, f"Technique Co-occurrence in {selected_category}")

if co_matrix is not None:
    masked_matrix = co_matrix.mask(np.tril(np.ones(co_matrix.shape)).astype(bool))
    max_pair = masked_matrix.stack().idxmax()
    max_value = masked_matrix.stack().max()

    context = "all categories" if selected_category == "All" else selected_category

    st.markdown(
        f"<p style='font-size:16px; margin-top: -10px;'>"
        f"The most common technique pair in <b>{context}</b> is <b>{max_pair[0]} + {max_pair[1]}</b> with <b>{max_value}</b> co-occurrences."
        f"</p>",
        unsafe_allow_html=True
    )

