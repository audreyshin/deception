import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title("Human Techniques for Deceiving AI in Outdraw AI")

st.markdown("""
For this part of the project I explore how humans are able to fool AI models like Gemini when drawing sketches. I went through incorrect guesses from the LLM and labeled techniques drawers used to confuse the AI. The purpose
            of this project is to see if there is any commanlities in the tecniques used to fool the AI model :D I analyzed 140 images which contained a few drawings from all 18 categories listed below. The dataset contained games played only in Singapore.

### Techniques of Deception
""")

st.markdown("""
- **Zoomed in texture** – Extremely close up view showing texture
- **Minimalist abstraction** – Uses very few lines to suggest the object or an outline of the object
- **Extraneous lines** – Irrelevant lines to distract the model
- **Misaligned feature** – Core features are placed strangely
- **Suggestive gesture** – Lines implying movement or intent
- **Implied scene** – Scene makes sense only when seen together
- **Overwriting motion** – Object is drawn then scribbled over
- **Odd perspective** – Blends multiple angles (top + side)
- **Culturally grounded** – Country specific references
- **Implied depth** – Uses tricks to show depth
- **Object decomposition** – Drawn in parts rather than whole
- **Stacked ambiguity** – Layered lines/objects add noise
""")

st.subheader(" Drawing Categories")

st.markdown("""
- **living_things**
- **actions**
- **types_of_people**
- **concepts**
- **types_of_places**
- **food_and_drink**
- **objects**
- **fiction**
- **famous places**
- **brands**
- **countries**
- **landmarks**
- **sports**
- **society_and_culture**
- **science_and_tech**
- **artists**
- **video_games**
- **movies**
""")



