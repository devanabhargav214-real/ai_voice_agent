import asyncio
import re
import streamlit as st
import edge_tts

# వెబ్‌సైట్ టైటిల్ మరియు డిజైన్
st.set_page_config(page_title="Telugu AI Voice", page_icon="🎙️")
st.title("🎙️ ఉచిత నాచురల్ తెలుగు AI వాయిస్ ఏజెంట్")
st.write("మీ పెద్ద స్క్రిప్ట్‌ను ఇక్కడ పేస్ట్ చేసి, నాచురల్ ఆడియోను డౌన్‌లోడ్ చేసుకోండి.")

# వాయిస్ సెలెక్షన్ ఆప్షన్స్
voice_option = st.selectbox(
    "వాయిస్ ఎంచుకోండి (Voice):",
    ("మగవారి వాయిస్ (Mohan Neural)", "ఆడవారి వాయిస్ (Shruti Neural)"),
)
voice = (
    "te-IN-MohanNeural"
    if "Mohan" in voice_option
    else "te-IN-ShrutiNeural"
)

# యూజర్ స్క్రిప్ట్ ఎంటర్ చేసే బాక్స్
script_text = st.text_area(
    "మీ స్క్రిప్ట్ ఇక్కడ టైప్ లేదా పేస్ట్ చేయండి:", height=250
)


def split_text(text, max_chars=1000):
    """పెద్ద స్క్రిప్ట్‌ను చిన్న భాగాలుగా విడగొట్టే ఫంక్షన్"""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ==========================================
# ఈ క్రింది ఫంక్షన్‌లో మార్పులు చేసాము (HIGHLIGHTED CHANGE)
# ==========================================
async def generate_audio(full_text, voice_model):
    """అన్‌లిమిటెడ్ టెక్స్ట్‌ను హై-క్వాలిటీ మరియు క్లియర్ ఆడియో కింద మార్చే ఫంక్షన్"""
    chunks = split_text(full_text)
    audio_data = b""

    # వాయిస్ క్వాలిటీ మరియు స్పష్టత పెంచడానికి స్పీడ్ 5% తగ్గించాం
    voice_speed = "-5%"
    voice_pitch = "+0Hz"

    for chunk in chunks:
        # ఇక్కడ rate మరియు pitch పారామీటర్లను యాడ్ చేశాం
        communicate = edge_tts.Communicate(
            chunk, voice_model, rate=voice_speed, pitch=voice_pitch
        )
        async for chunk_data in communicate.stream():
            if chunk_data["type"] == "audio":
                audio_data += chunk_data["data"]

    return audio_data


# ==========================================

# జనరేట్ బటన్ క్లిక్ చేసినప్పుడు
if st.button("AI వాయిస్ జనరేట్ చేయి 🚀"):
    if script_text.strip() == "":
        st.warning("దయచేసి ఏదైనా స్క్రిప్ట్ టైప్ చేయండి!")
    else:
        with st.spinner("AI వాయిస్ జనరేట్ అవుతోంది... దయచేసి ఆగండి..."):
            try:
                # అసింక్రోనస్ లూప్ రన్ చేయడం
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                final_audio_bytes = loop.run_until_complete(
                    generate_audio(script_text, voice)
                )

                # ఆడియో ప్లేయర్ మరియు డౌన్‌లోడ్ ఆప్షన్
                st.audio(final_audio_bytes, format="audio/mp3")
                st.download_button(
                    label="📥 ఆడియో ఫైల్ డౌన్‌లోడ్ చేసుకోండి",
                    data=final_audio_bytes,
                    file_name="telugu_ai_voice.mp3",
                    mime="audio/mp3",
                )
                st.success("వాయిస్ విజయవంతంగా జనరేట్ అయింది!")
            except Exception as e:
                st.error(f"చిన్న లోపం వచ్చింది: {e}")
