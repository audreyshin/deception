import streamlit as st
import pandas as pd

sheet_url = "https://docs.google.com/spreadsheets/d/1nGRDV27Wz3Xf3jfD_rlEsTeFebSAhFsnYYMMhbeO_jc/export?format=csv"
df = pd.read_csv(sheet_url)

# Drop completely empty rows
df = df.dropna(how="all").reset_index(drop=True)

total_images = len(df)   # should now be 919



st.set_page_config(page_title="Outdraw AI | Research Homepage", layout="wide")
# === Map category ID to name ===
id_to_name = {
    55: "living_things", 56: "actions", 57: "types_of_people", 58: "concepts",
    59: "types_of_places", 60: "food_and_drink", 61: "objects", 62: "fiction",
    63: "famous places", 64: "brands", 65: "countries", 66: "landmarks",
    67: "sports", 68: "society_and_culture", 69: "science_and_tech",
    70: "artists", 71: "video_games", 72: "movies"
}
df["category_name"] = df["category_id"].map(id_to_name)

# === TITLE ===
st.title("Human Drawing Techniques in Decieving AI")


st.markdown("""
This project explores how humans can consistently fool LLMs like **Gemini** in cooperative sketch guessing games. All data comes from different rounds of the Deviation Game (formerly known as outdraw.AI a game that pits human creativity against AI perception. 
""")

st.markdown("""
<div style="background-color: #f9f2f4; padding: 15px; border-left: 5px solid #e75480; border-radius: 5px;">
<p style="margin-bottom: 0;">
<strong>Goal:</strong> Uncover drawing techniques that confuse the model while remaining clear to humans.
</p>
</div>
""", unsafe_allow_html=True)

# Set up 3 columns for layout
col1, col2, col3 = st.columns(3)

# === EXAMPLE BLOCK ===
with col1:
    st.image("drawings_by_category/58/58_2.jpg", use_container_width=True)
    st.markdown("""
    <div style="text-align: center; font-size: 14px;">
        <b>Ground Truth:</b> Art<br>
         <b>AI Guess:</b> Mess<br>
    
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("drawings_by_category/55/55_51.jpg", use_container_width=True)
    st.markdown("""
    <div style="text-align: center; font-size: 14px;">
         <b>Ground Truth:</b> Goldfish<br>
        <b>AI Guess:</b> kitten<br>
         
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("drawings_by_category/56/56_16.jpg", use_container_width=True)
    st.markdown("""
    <div style="text-align: center; font-size: 14px;">
         <b>Ground Truth:</b> dribbling<br>
         <b>AI Guess:</b> playing<br>
        
    </div>
    """, unsafe_allow_html=True)
# === SECTION: Project Overview ===

st.subheader("Research Motivation")

st.markdown("""
I began this investigation using a dataset containing games played only in Singapore. However, I pivoted shortly after and refined some of my earlier methods.
During this trial run, I was looking at games where the result was labeled as **"AI_LOSE_COMPLETELY"**. But I was under the false presumption that this meant at least one human guessed correctly and the AI didn’t. In reality, that label just meant the AI was completely wrong across all of its guesses. The LLM works by generating multiple guesses for each drawing and picking the one with the highest confidence.

For the second trial run, I switched datasets and used a different filtering process. This time, I made sure to only include rows where **the AI guessed incorrectly** but **at least one human got it right**.
The motivation here is to figure out, how are humans able to draw in ways that throw off LLMs, while still being interpretable by other humans? I looked through the AI justification for choosing its wrong answer
            to determine what specific technique a human used to fool the LLM.

The dataset I used is called the **Exploratorium Dataset**, which originally contained about 23,000 rows. I augmented it by extracting additional info from each drawing's JSON and added the following columns:
- AI guess
- Confidence score
- Reasoning

""")


# === SECTION: Final Dataset Pipeline ===
st.subheader(" Data Filtering Pipeline")

st.markdown("""
To construct my final dataset of **857 clean examples**, I followed this process:
""")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.graphviz_chart("""
    digraph {
        node [shape=box, style="filled", fillcolor="#fbe4ed"];  // soft pink

        raw_data [label="Raw Dataset (23000+ games)"]
        filter_results [label="Filter: result ∈ {AI_LOSE_COMPLETELY, AI_LOSE_MARGINAL}"]
        extract_ai [label="Fetch AI guess, confidence, reasoning from JSON"]
        normalize [label="Normalize human guesses + match to ground truth"]
        filter_correct_human [label="Keep if humans guessed correctly"]
        drop_nulls [label="Drop if AI guess is null"]
        final_data [label="Final Labeled Set (857 rows)"]

        raw_data -> filter_results -> extract_ai -> normalize -> filter_correct_human -> drop_nulls -> final_data
    }
    """)


st.subheader("Final Filtering Query")

st.markdown("""
Below is the SQL query used to filter the final dataset of drawings where the AI failed but at least one human guessed correctly:

```sql
SELECT *
FROM exporatorium_augmented
WHERE result IN ('AI_LOSE_COMPLETELY', 'AI_LOSE_MARGINAL')
  AND human_guessed_correctly = TRUE
  AND ai_guess IS NOT NULL;
""")

st.markdown("""
This cleaned dataset reflects cases where the AI made confident but ultimately incorrect guesses, while humans correctly identified the drawing.
Specifically, I filtered for results labeled as either **"AI_LOSE_COMPLETELY"** (none of the AI’s guesses were correct) or **"AI_LOSE_MARGINAL"** (the correct answer was somewhere in the AI's top guesses, but not selected as its final answer).
In other words, these are drawings where the model may have *considered* the right answer, but ultimately chose something else with more confidence. Meanwhile, human players were able to guess the correct answer from the same sketch.
These examples are a useful starting point for analyzing where human perception and AI visually diverge.
""")


# === SECTION: Techniques ===
st.subheader("Techniques Humans Use to Fool AI")
st.markdown("Below are techniques I observed that consistently confused the AI model:")

techniques = {
    "Atypical Representation": "Deviations from canonical forms (e.g., triangle for a head).",
    "Culturally Grounded": "Includes regional or cultural references.",
    "Extraneous Lines": "Irrelevant markings added to confuse the AI.",
    "Implied Depth": "Visual cues like nesting or perspective to simulate 3D.",
    "Implied Scene": "Context only makes sense when elements are interpreted as a whole.",
    "Invalid Test Result": "This includes test rounds, obvious cheating, or invalid entries.",
    "Minimalist Abstraction": "Sparse lines that suggest form without explicit detail. An outline of the object.",
    "Misaligned Feature": "Core parts placed incorrectly, like a leg coming out of a chin or face in the wrong place. Disproportionate sizing.",
    "Object Decomposition": "Drawn in parts, not as a whole — breaking down template-matching techniques.",
    "Odd Perspective": "Mixing top-down and side views.",
    "Overwriting Motion": "Object drawn, then scribbled over to confuse the AI.",
    "Stacked Ambiguity": "Overlapping or layered content creates noise.",
    "Suggestive Gesture": "Expressive strokes implying movement or intent.",
    "Zoomed-in Texture": "Close up views focusing on texture instead of form."
}

# Manually assign examples
examples = {
    "Atypical Representation": {
        "image_path": "drawings_by_category/55/55_13.jpg",
        "ground_truth": "panda",
        "ai_guess": "unicorn",
        "notes": "Triangle used for the panda's ear caused confusion."
    },
    "Minimalist Abstraction": {
        "image_path": "drawings_by_category/55/55_11.jpg",
        "ground_truth": "cat",
        "ai_guess": "blobfish",
        "notes": "The cartoonish drawing of a cat with the circles representing the eyes, and mouth area of the cat, threw off the LLM into thinking it was a blobfish."
    },
    "Extraneous Lines": {
        "image_path": "drawings_by_category/55/55_25.jpg",
        "ground_truth": "parrot",
        "ai_guess": "lamprey",
        "notes": "The addition of a lines at the bottom were misinterpreted as a stream, causing the LLM into thinking the parrot was a lamprey."
    },
     "Culturally Grounded": {
        "image_path": "images/59/59_1.jpg",
        "ground_truth": "bank",
        "ai_guess": "SCP foundation",
        "notes": "SGD at the top of the structure symbolizes singapore dollars. This particular round was played in Singapore"
    },
    "Implied Depth": {
        "image_path": "images/59/59_5.jpg",
        "ground_truth": "cave",
        "ai_guess": "Cabin",
        "notes": "Rectangles inside each other show the depth of the cave."
    },
    "Implied Scene": {
        "image_path": "drawings_by_category/55/55_6.jpg",
        "ground_truth": "caterpillar",
        "ai_guess": "sea cucumber",
        "notes": "The metapmorophasis of a butterfly was misinterpreted by AI. Some parts of the drawing were completely ignored so the AI guess just took into account the catipillar at the bottom."
    },
    "Suggestive Gesture": {
        "image_path": "drawings_by_category/56/56_8.jpg",
        "ground_truth": "jumping",
        "ai_guess": "gliding",
        "notes": "The lines motioning upwards show a jumping movement but the LLM misinterpreted this."
    },
    "Invalid Test Result": {
        "image_path": "drawings_by_category/55/55_0.jpg",
        "ground_truth": "mouse",
        "ai_guess": "aardvark",
        "notes": "Nothing of meaning was drawn in the first place, just a bunch of scribbles"
    },
    "Overwriting Motion": {
        "image_path": "drawings_by_category/55/55_9.jpg",
        "ground_truth": "goldfish",
        "ai_guess": "squid",
        "notes": "The original drawing can be classified as a goldfish but was later scribbled over by the drawer to decieve the LLM."
    },
    "Misaligned Feature": {
        "image_path": "drawings_by_category/55/55_17.jpg",
        "ground_truth": "walrus",
        "ai_guess": "tadpole",
        "notes": "The misaligned features, the off proportions of the walrus helped humans guess correctly but threw off the LLM."
    },
    "Object Decomposition": {
        "image_path": "images/60/60_6.jpg",
        "ground_truth": "melon",
        "ai_guess": "soda",
        "notes": "Object is in a different form throwing off the AI."
    },
     "Odd Perspective": {
        "image_path": "images/59/59_2.jpg",
        "ground_truth": "bowling alley",
        "ai_guess": "water park",
        "notes": "The different combined perspectives of the bowling alley threw off the LLM."
    },
     "Zoomed-in Texture": {
        "image_path": "images/69/69_0.jpg",
        "ground_truth": "asteroid",
        "ai_guess": "virus",
        "notes": "The texture on the asteroid is misinterpreted when zoomed in."
    },
     "Stacked Ambiguity": {
        "image_path": "images/60/60_8.jpg",
        "ground_truth": "french fries",
        "ai_guess": "lattice pie",
        "notes": "The layering threw off the LLM."
    },
 
    # Add the rest...
}



col1, col2 = st.columns(2)
technique_items = sorted(techniques.items())

for i, (technique, description) in enumerate(technique_items):
    col = col1 if i % 2 == 0 else col2
    with col.expander(f"{technique}"):
        st.markdown(f"<div style='padding: 10px; font-size: 15px;'>{description}</div>", unsafe_allow_html=True)

        if technique in examples:
            ex = examples[technique]
            st.image(ex["image_path"], use_container_width=True)
            st.markdown(f"**Ground Truth:** {ex['ground_truth']}")
            st.markdown(f"**AI Guess:** {ex['ai_guess']}")
            st.markdown(f"**Notes:** {ex['notes']}")
        else:
            st.markdown("*No example added yet.*")


st.markdown("""
<div style='
    background-color: #f9f2f4;
    padding: 15px 15px 25px 15px;  /* top right bottom left */
    border-left: 5px solid #e75480;
    border-radius: 5px;
'>
<p style="margin-bottom: 0;">
         <strong>Note:</strong> Drawings can include multiple techniques!
</p>
</div>
""", unsafe_allow_html=True)


# === SECTION: Labeling Progress ===
st.subheader("Labeling Progress")

# make sure category_id is numeric before mapping (prevents dropouts)
df["category_id"] = pd.to_numeric(df["category_id"], errors="coerce")

# Count only rows where ai_guess is not empty/blank
mask_valid = df["ai_guess"].notna() & (df["ai_guess"].astype(str).str.strip() != "")
df_valid = df[mask_valid]

total_images = len(df_valid)                    
analyzed_images = df_valid["technique_used"].notna().sum()
percent_done = (analyzed_images / total_images) * 100

st.markdown(
    f"<p style='font-size:16px;'>"
    f"<b>{analyzed_images}</b> out of <b>{total_images}</b> drawings have been labeled "
    f"({percent_done:.1f}%)."
    f"</p>",
    unsafe_allow_html=True
)

def pink_progress_bar(label, value, max_value=100):
    percent = int((value / max_value) * 100)
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <div style="font-size: 15px; margin-bottom: 4px;">{label} — {value} / {max_value} ({percent}%)</div>
        <div style="background-color: #f0f0f0; border-radius: 10px; height: 10px; width: 100%;">
            <div style="
                background-color: #e75480;
                width: {percent}%;
                height: 100%;
                border-radius: 10px;
                transition: width 0.3s ease;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Count totals per category
category_totals = df["category_name"].value_counts().to_dict()
category_labeled = df[df["technique_used"].notna()]["category_name"].value_counts().to_dict()

# Show progress bar for each category
for category in sorted(id_to_name.values()):
    total = category_totals.get(category, 0)
    labeled = category_labeled.get(category, 0)

    if total > 0:
    
        pink_progress_bar(category.replace('_', ' ').title(), labeled, total)

    else:
        st.markdown(f"**{category.replace('_', ' ').title()}** — No data available")


st.markdown("""This is still very much a work in progress. I haven't finished labeling all the images yet but use the progress bars to gauge the accuracy of the results displayed.""")
st.subheader("Notes")

st.markdown("""
Out of over 23,000 Outdraw games (with some margin of error for rounds with incomplete data), only about 1,000 cases showed a clear divergence, where humans guessed correctly and the AI did not.
This suggests that in the vast majority of cases, the AI was able to interpret drawings in ways that losely mirror human perception.
It’s these rare failure cases that are most revealing. Analyzing them exposes the limits of AI reasoning and helps us understand which human techniques break AI understanding, even when other humans still interpret the sketch with ease.
""")
