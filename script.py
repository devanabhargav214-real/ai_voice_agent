import streamlit as st
import os
from crewai import Agent, Task, Crew, Process, LLM

# Streamlit పేజీ సెటప్
st.set_page_config(page_title="AI తెలుగు కథలు", page_icon="📖", layout="centered")

st.title("📖 AI తెలుగు కథల జనరేటర్")
st.write("టాపిక్ ఎంటర్ చేసి 'కథను సిద్ధం చేయి' బటన్ క్లిక్ చేయండి.")

# మీ API Key ని Streamlit Secrets నుండి బ్యాక్‌గ్రౌండ్‌లోనే సెట్ చేయడం
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Streamlit Secrets లో GEMINI_API_KEY కాన్ఫిగర్ చేయలేదు!")

# కస్టమర్ కేవలం టాపిక్ మాత్రమే ఇస్తారు
user_prompt = st.text_input("కథ దేని గురించి రాయాలి? (Topic/Idea):", 
                            placeholder="ఉదాహరణ: తెనాలి రామకృష్ణ కథలు, ఒక తెలివైన కాకి...")

if st.button("🚀 కథను సిద్ధం చేయి"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("API Key అందుబాటులో లేదు. దయచేసి సెట్టింగ్స్ చెక్ చేయండి.")
    elif not user_prompt:
        st.warning("కథ రాయడానికి ఏదైనా ఒక టాపిక్ ఇవ్వండి!")
    else:
        with st.spinner("🤖 AI ఏజెంట్ కథను ఆలోచిస్తోంది... కాసేపు ఆగండి..."):
            try:
                # LLM కాన్ఫిగరేషన్
                gemini_llm = LLM(
                    model="gemini/gemini-1.5-flash",
                    temperature=0.7
                )

                # AI Agent సెటప్
                story_writer = Agent(
                    role='Senior Telugu Story Teller',
                    goal='주어진 లైన్ ఆధారంగా అద్భుతమైన, నీతి గల తెలుగు కథలను రాయడం.',
                    backstory='''nuvvu తెలుగు సాహిత్యం మరియు జానపద కథలలో నిపుణుడివి. 
                    నువ్వు రాసే కథలలో పాత్రలు, భావోద్వేగాలు మరియు చక్కటి తెలుగు పదజాలం ఉంటాయి. 
                    కథ ముగింపులో మంచి నీతి (Moral) ఉంటుంది.''',
                    verbose=True,
                    llm=gemini_llm
                )

                # టాస్క్ క్రియేషన్
                story_task = Task(
                    description=f'''టాపిక్: "{user_prompt}". 
                    ఈ టాపిక్ ఆధారంగా ఒక ఆసక్తికరమైన తెలుగు కథను రాయండి. 
                    కథలో పరిచయం, మలుపులు (twists), మరియు ఒక మంచి ముగింపు ఉండాలి.''',
                    expected_output='చక్కటి తెలుగు ఫాంట్ మరియు పారాగ్రాఫ్‌లతో కూడిన ఒక పూర్తి కథ మరియు దాని నీతి.',
                    agent=story_writer
                )

                # Crew రన్ చేయడం
                story_crew = Crew(
                    agents=[story_writer],
                    tasks=[story_task],
                    process=Process.sequential
                )

                result = story_crew.kickoff()
                
                # రిజల్ట్ డిస్ప్లే
                st.success("✨ మీ కథ సిద్ధంగా ఉంది! ✨")
                st.markdown("---")
                st.markdown(result.raw)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"ఏదో తప్పు జరిగింది: {e}")
                
