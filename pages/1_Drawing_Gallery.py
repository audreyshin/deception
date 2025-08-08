import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

# === Scroll to top after page change ===
if "scroll_to_top" not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    st.markdown(
        """
        <script>
            window.scrollTo({top: 0, behavior: 'instant'});
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state.scroll_to_top = False  # reset

# === Live Google Sheet CSV ===
csv_url = "https://docs.google.com/spreadsheets/d/1nGRDV27Wz3Xf3jfD_rlEsTeFebSAhFsnYYMMhbeO_jc/export?format=csv"
df = pd.read_csv(csv_url)

# === Map category ID to human-readable name ===
id_to_name = {
    55: "living_things", 56: "actions", 57: "types_of_people", 58: "concepts",
    59: "types_of_places", 60: "food_and_drink", 61: "objects", 62: "fiction",
    63: "famous places", 64: "brands", 65: "countries", 66: "landmarks",
    67: "sports", 68: "society_and_culture", 69: "science_and_tech",
    70: "artists", 71: "video_games", 72: "movies"
}
df["category_name"] = df["category_id"].map(id_to_name)

# === Parse date ===
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

# === Page title ===
st.title("Drawings Deceptive to AI")

# === Sidebar Filters ===
with st.sidebar:
    st.header("Filters")

    # --- CATEGORY SINGLE SELECT ---
    all_categories = sorted(df["category_name"].dropna().unique())
    selected_category = st.selectbox("Choose Category", ["All"] + all_categories)
    if selected_category != "All":
        filtered_df = df[df["category_name"] == selected_category].copy()
    else:
        filtered_df = df.copy()

    # --- TECHNIQUE SELECTBOX ---
    technique_options = set()
    filtered_df["technique_used"].dropna().apply(
        lambda x: [technique_options.add(t.strip()) for t in x.split(",")]
    )
    selected_technique = st.selectbox("Technique", ["All"] + sorted(technique_options))
    if selected_technique != "All":
        filtered_df = filtered_df[filtered_df["technique_used"].str.contains(selected_technique, na=False)]

    # --- HAS NOTES CHECKBOX ---
    if st.checkbox("Only show drawings with notes"):
        filtered_df = filtered_df[filtered_df["notes"].notnull() & (filtered_df["notes"].str.strip().str.lower() != "nan")]

    # --- FILTER OUT INVALID TEST RESULTS ---
    if st.checkbox("Filter out invalid test results", value=True):
        filtered_df = filtered_df[
            filtered_df["technique_used"].str.strip().str.lower() != "invalid test result"
        ]


    # --- DATE GRANULARITY ---
    st.markdown("**Date Range**")
    date_filter_mode = st.radio("View", ["All Time", "This Month", "This Week", "Custom Range"], index=0)

    now = pd.Timestamp.now(tz="UTC")
    if date_filter_mode == "This Month":
        start_date = now.replace(day=1)
        end_date = now
    elif date_filter_mode == "This Week":
        start_date = now - pd.Timedelta(days=7)
        end_date = now
    elif date_filter_mode == "Custom Range":
        min_date = filtered_df["created_at"].min()
        max_date = filtered_df["created_at"].max()
        start_date, end_date = st.date_input("Select Range", [min_date, max_date])
        start_date = pd.to_datetime(start_date).tz_localize("UTC")
        end_date = pd.to_datetime(end_date).tz_localize("UTC")
    else:
        start_date, end_date = None, None

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["created_at"] >= start_date) &
            (filtered_df["created_at"] <= end_date)
        ]

    # --- AI CONFIDENCE SLIDER ---
    min_conf, max_conf = int(filtered_df["ai_confidence"].min()), int(filtered_df["ai_confidence"].max())
    conf_range = st.slider("AI Confidence", min_conf, max_conf, (min_conf, max_conf))
    filtered_df = filtered_df[
        (filtered_df["ai_confidence"] >= conf_range[0]) &
        (filtered_df["ai_confidence"] <= conf_range[1])
    ]

    # --- RESET BUTTON ---
    if st.button("Reset Filters"):
        st.rerun()

# === Sort by whether notes exist ===
filtered_df["has_notes"] = filtered_df["notes"].notnull() & (filtered_df["notes"].str.strip().str.lower() != "nan")
filtered_df = filtered_df.sort_values(by="has_notes", ascending=False)

# === Pagination ===
PAGE_SIZE = 20
total_rows = len(filtered_df)
total_pages = (total_rows - 1) // PAGE_SIZE + 1

if "page_num" not in st.session_state:
    st.session_state.page_num = 0

start_idx = st.session_state.page_num * PAGE_SIZE
end_idx = start_idx + PAGE_SIZE
page_df = filtered_df.iloc[start_idx:end_idx]

st.caption(f"Page {st.session_state.page_num + 1} of {total_pages}")
st.subheader(f"{len(filtered_df)} Drawings in {selected_category if selected_category != 'All' else 'All Categories'}")

# === Image Display ===
cols = st.columns(3)
for i, (_, row) in enumerate(page_df.iterrows()):
    col = cols[i % 3]
    with col:
        category_folder = str(row["category_id"])
        image_path = os.path.join("drawings_by_category", category_folder, os.path.basename(row["image_path"]))

        if os.path.exists(image_path):
            st.image(Image.open(image_path), caption=row["ground_truth"], use_container_width=True)
            st.markdown(f"`{row['technique_used']}`")

            if "ai_guess" in row and pd.notnull(row["ai_guess"]):
                st.markdown(f"**AI Guess**: {row['ai_guess']}")

            if "ai_justification" in row and pd.notnull(row["ai_justification"]):
                st.markdown(f"**AI Reasoning**: {row['ai_justification']}")

            if "human_guesses" in row and pd.notnull(row["human_guesses"]):
                st.markdown(f"**Human Guesses**: {row['human_guesses']}")

            notes = str(row["notes"]).strip()
            if notes and notes.lower() != "nan":
                st.markdown(f"**Notes**: {notes}")

            st.caption(f"Date: {row['created_at'].date()}")
        else:
            st.warning(f"Image not found: {image_path}")

# === Pagination Buttons at Bottom ===
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button(" Prev", key="prev") and st.session_state.page_num > 0:
        st.session_state.page_num -= 1
        st.session_state.scroll_to_top = True
        st.rerun()

with col3:
    if st.button("Next", key="next") and st.session_state.page_num < total_pages - 1:
        st.session_state.page_num += 1
        st.session_state.scroll_to_top = True
        st.rerun()
