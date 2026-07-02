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

# --- కొత్త ఫీచర్లు: స్పీడ్ మరియు వాల్యూమ్ కంట్రోల్స్ ---
st.write("### 🎛️ వాయిస్ సెట్టింగ్స్ (Voice Controls):")
col1, col2 = st.columns(2)

with col1:
    # స్పీడ్ స్లైడర్ (నార్మల్ స్పీడ్ 0%. పెంచడానికి +, తగ్గించడానికి -)
    speed_slider = st.slider(
        "వాయిస్ వేగం (Speed):",
        min_value=-50,
        max_value=50,
        value=-5,
        step=5,
        format="%d%%",
    )
    voice_speed = f"{'' if speed_slider < 0 else '+'}{speed_slider}%"

with col2:
    # వాల్యూమ్ స్లైడర్ (నార్మల్ వాల్యూమ్ 0%. పెంచడానికి +, తగ్గించడానికి -)
    volume_slider = st.slider(
        "వాల్యూమ్ స్థాయి (Volume):",
        min_value=-50,
        max_value=50,
        value=0,
        step=5,
        format="%d%%",
    )
    voice_volume = f"{'' if volume_slider < 0 else '+'}{volume_slider}%"
# ---------------------------------------------

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


async def generate_audio(full_text, voice_model, speed, volume):
    """అన్‌లిమిటెడ్ టెక్స్ట్‌ను హై-క్వాలిటీ ఆడియో కింద మార్చే ఫంక్షన్"""
    chunks = split_text(full_text)
    audio_data = b""

    for chunk in chunks:
        # ఇక్కడ rate మరియు volume ని డైనమిక్ గా పాస్ చేస్తున్నాం
        communicate = edge_tts.Communicate(
            chunk, voice_model, rate=speed, volume=volume
        )
        async for chunk_data in communicate.stream():
            if chunk_data["type"] == "audio":
                audio_data += chunk_data["data"]

    return audio_data


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
                    generate_audio(script_text, voice, voice_speed, voice_volume)
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
                
