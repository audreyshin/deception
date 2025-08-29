# === FUTURE WORK SECTION (drop this anywhere in your Streamlit script) ===
import json
import streamlit as st

st.markdown("## Initial Findings ✧˖° ")
st.markdown("""
- The most popular technique was **minimalist abstraction**. Simple drawings with only a few strokes (like a cube meant to be an ice cube) were often very hard to interpret. These cases felt like luck, humans sometimes guessed right, but the AI often made a slightly off but reasonable guess.
- Users employed a wide range of deception strategies including scribbling/overdraw, spikes in stroke density, exaggerated or distorted shapes, ambiguous minimal drawings, and added distractors. These consistently reduced model confidence or induced misclassification.
- Techniques that increased clutter or stroke density often pushed models into either **wrong high confidence guesses** or **low confidence abstentions**.
- Ambiguity was effective: underspecified drawings and blended shapes that could hint at multiple categories were particularly difficult for the AI.
""")
st.markdown("## Future Directions")
st.markdown("""
- First priority is to **revisit items labeled as “unsure”**, especially in the *Countries* category.  
    - Future reviewers should check whether certain drawings are **culturally grounded** and may only be correctly understood by people from that background.  
    - Keep a lightweight adjudication log (who reviewed, when, and why) so the process is reproducible.

- **Improve preprocessing** by filtering out gibberish or non intentional doodles before analysis.  
    - A filtering step could use heuristics like stroke count/entropy, connected components, contour complexity, or lightweight CNN baselines.  
    - References:  
        - [Paper 1](https://www.proquest.com/openview/ae34c2714bc7b02c0d83c67cb3f19670/1?cbl=2035040&pq-origsite=gscholar)  
        - [Book on preprocessing](https://books.google.com/books?hl=en&lr=&id=0AmhDwAAQBAJ&oi=fnd&pg=PA1&dq=sketch+recognition+noise+reduction+preprocessing&ots=sre_c0oizQ&sig=_0CMOvmlrvbFLrnglwKC-apo1xc#v=onepage&q&f=false)  
        - [Article 1](https://www.sciencedirect.com/science/article/abs/pii/S0925231219309324)  
        - [Book 2](https://www.taylorfrancis.com/books/mono/10.1201/9780203903896/pattern-recognition-image-preprocessing-sing-bow)  
        - [Article 2](https://www.sciencedirect.com/science/article/abs/pii/S0167865514000257)

- To make results more **conclusive**, analysis should not only study failures but also look at where the AI **got things right**.  
    - Compute ratios of right vs. wrong classifications per technique.  
    - This will help determine whether a strategy truly fools the AI in most cases, or if it was only missed occasionally.

- **Language and text based strategies** deserve finer categorization:  
    - Word equations  
    - Use of different languages or scripts  
    - Backwards or mirrored spelling  
    - Equations that mix pictures and text  
    - Adding irrelevant words to mislead  
    - Drawings where a full object is drawn but arrows/cross outs direct attention to a sub part (sometimes misread as just lines by the AI)

- **Abstraction and symbolism** should be studied more systematically:  
    - Cases like drawing “ice” to mean “Iceland” require multi step reasoning.  
    - Minimalist abstractions often confused both humans and AI, but humans sometimes guessed correctly by chance.  
    - These examples show how fragile both human and AI interpretation can be when detail is minimal.
""")





st.markdown("## Takeaways")
st.markdown("""
My main takeaway is that it takes effort from many countries and perspectives to really push this research forward. 
Diversity in training data is essential, yet it also reveals the impossibility of capturing differences without, in some way, also integrating our biases. 
That tension is at the heart of fairness in AI: cultural depth and abstraction require exposure to perspectives, but those perspectives themselves are never neutral. 
I found it fascinating how models sometimes miss what humans see, for example, one drawing meant to represent *diversity* was interpreted simply as *community*, showing both a blindness and a simplification of human meaning. 
This challenge makes me optimistic, though: as the field expands, there is a chance to move toward systems that not only reflect but also support humanity more equitably. 
I’m excited to see how future work can strengthen AI’s ability to interpret with nuance, fairness, and empathy.
""")


