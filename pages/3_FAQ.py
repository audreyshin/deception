import streamlit as st

st.set_page_config(page_title="FAQ | Outdraw AI", layout="wide")

st.title("Frequently Asked Questions")

# Add some spacing
st.markdown("---")

# FAQ 1
with st.expander("**What’s the difference between Overwriting Motion and an Invalid Test Result?**", expanded=False):
    st.markdown("""
    If the scribble was added *after* seeing the answer (like in a test round), it’s labeled as an **Invalid Test Result**.

    But if the drawer first created a valid image and then scribbled over it *as part of the drawing*, it's considered **Overwriting Motion**.
    """)
