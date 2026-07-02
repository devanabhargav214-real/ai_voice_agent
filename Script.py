import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Free AI తెలుగు కథలు", page_icon="📖")
st.title("📖 ఉచిత AI తెలుగు కథల జనరేటర్ (No API Key)")

user_prompt = st.text_input("కథ టాపిక్ ఇవ్వండి:")

if st.button("🚀 కథను సిద్ధం చేయి"):
    if user_prompt:
        with st.spinner("కథను సిద్ధం చేస్తున్నాను..."):
            try:
                # Hugging Face నుండి ఉచితంగా మోడల్ ని లోడ్ చేయడం
                # గమనిక: ఇది Streamlit Cloud లో లోడ్ అవ్వడానికి 2-3 నిమిషాలు పడుతుంది
                pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B-Instruct")
                
                messages = [
                    {"role": "system", "content": "నువ్వు ఒక తెలుగు కథకుడివి. కేవలం తెలుగులోనే సమాధానం ఇవ్వాలి."},
                    {"role": "user", "content": f"{user_prompt} అనే టాపిక్ మీద ఒక చిన్న నీతి కథ రాయు."}
                ]
                
                response = pipe(messages, max_new_tokens=500)
                story = response[0]['generated_text'][-1]['content']
                
                st.success("✨ మీ కథ:")
                st.write(story)
            except Exception as e:
                st.error(f"Error: {e}")
