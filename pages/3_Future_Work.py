import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from itertools import combinations
import numpy as np

import streamlit as st

st.markdown("""
# Initial Findings

- **Technique diversity:** Users employed a range of deception strategies (scribbling/overdraw, stroke density spikes, exaggerated or distorted shapes, minimal-stroke ambiguity, and added distractors) that consistently reduced model confidence or induced misclassification.
- **Mode sensitivity:** Techniques that increase **stroke density** or **visual clutter** tended to push models toward either incorrect high-confidence guesses or low-confidence abstentions.
- **Ambiguity wins:** Deliberately **underspecified** drawings (very few strokes) and **shape blending** (hinting at multiple categories) were particularly effective.
- **Human notes matter:** Free-text notes often revealed intent (e.g., “made it messy to confuse it”), which aligned with lower model confidence; pairing qualitative notes with quantitative confidence shifted analysis from guess-only to **strategy-aware** evaluation.

---

# Future Work

## 1) Collaborative Categorization & Reliability
- Thus far, categorization was completed by a single researcher. To strengthen validity:
  - Recruit multiple researchers to independently **review and recategorize** techniques.
  - Compute **inter-rater reliability** (e.g., Cohen’s κ / Krippendorff’s α) and reconcile disagreements.
  - Produce a **final taxonomy** with clear definitions and positive/negative examples.

### 1.1) Targeted Review of “Unsure” Items
- Wherever entries are **marked as *unsure*** in the dataset, future UROPs or project members should **revisit and attempt classification** using the refined taxonomy.
- Keep a lightweight **adjudication log** (date, reviewer, rationale) so decisions are auditable and reproducible.

## 2) Expanding Across Datasets
- Apply the same labeling and analysis pipeline to:
  - **Singapore dataset** (next priority)
  - Additional incoming datasets over time
- Compare **technique prevalence** and **model vulnerability** across datasets (e.g., cultural style differences, stroke order norms) to test generalizability.

## 3) Filtering Gibberish / Non-Intentional Inputs
- Improve preprocessing by excluding **gibberish** or non-intentional doodles before analysis:
  - Train a lightweight **CNN** (or MobileNet/EfficientNet variant) to separate meaningful sketches from noise.
  - Features to explore: stroke count/entropy, connected-component stats, contour complexity, and frequency-domain signals.
- Seed reading list (replace with your links):
  - [Placeholder: CNN baseline for sketch/noise filtering]
  - [Placeholder: Lightweight architectures for mobile inference]
  - [Placeholder: Stroke-feature heuristics vs. learned filters]

## 4) Category Tree for Deception Techniques (Draft)
A living taxonomy to organize strategies; refine through collaborative review and empirical tests.


- Each node should have: **definition**, **inclusion/exclusion criteria**, **examples**, and **known model effects** (confidence shift, mislabel tendency).
- Consider linking nodes to **dashboard filters** so reviewers can browse by branch.

## 5) Reference & Live Demo
- Technique gallery (current app): https://deception-fhjfvnqyteaeqq7acroxol.streamlit.app
- Add a “**Research Starter Pack**” section in the app sidebar with method links, taxonomy docs, and labeling guidelines.

---
**Implementation Notes (next iteration)**
- Add a **review queue** view filtered to `unsure == True`.
- Log reviewer actions to a small table (`review_events`) with timestamps.
- Store versioned taxonomy in the repo and surface it in-app for quick reference.
""")
