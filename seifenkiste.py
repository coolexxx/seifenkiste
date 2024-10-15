import streamlit as st
import os
from openai import OpenAI
import tempfile

# OpenAI-Client initialisieren mit Streamlit Secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

def transkribiere_audio(audio_datei, zielsprache):
    try:
        transkription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_datei,
            language=zielsprache
        )
        return transkription.text
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"

st.set_page_config(page_title="Seifenkiste: Audio to Text", page_icon="🎙️", layout="centered")

st.title("🎙️ Seifenkiste: Audio to Text")

st.markdown("""
Diese App ermöglicht es, Audiodateien hochzuladen und sie mithilfe des OpenAI Whisper-Modells zu transkribieren.
""")

sprachen = {
    "Deutsch": "de",
    "Englisch": "en",
    "Französisch": "fr",
    "Spanisch": "es",
    "Italienisch": "it"
}

ausgewaehlte_sprache = st.selectbox(
    "Wählen Sie die Sprache der Audiodatei:",
    list(sprachen.keys())
)

hochgeladene_datei = st.file_uploader("Wählen Sie eine Audiodatei", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])

if hochgeladene_datei is not None:
    st.audio(hochgeladene_datei, format="audio/wav")
    
    if st.button("Audio transkribieren"):
        with st.spinner("Transkribiere..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{hochgeladene_datei.name.split('.')[-1]}") as temp_datei:
                temp_datei.write(hochgeladene_datei.getvalue())
                temp_datei_pfad = temp_datei.name

            with open(temp_datei_pfad, "rb") as audio_datei:
                transkription = transkribiere_audio(audio_datei, sprachen[ausgewaehlte_sprache])

            os.unlink(temp_datei_pfad)

        st.success("Transkription abgeschlossen!")
        st.text_area("Transkription", transkription, height=300)

st.markdown("---")
st.markdown("Made by Alex")
