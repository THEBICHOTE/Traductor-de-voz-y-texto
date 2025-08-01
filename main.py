import gradio as gradio
import whisper
from deep_translator import GoogleTranslator 
from gTTS import gTTS
import tempfile
import os

# Cargamos el modelo Whisper (Tiny este es el mas liviano)
whisper_model = whisper.load_model("Tiny")

#Funcion Principal 
def translate_input(audio_file, text_input, target_lang, voice_choice) :
    try:
        #obtener el texto (se Voz o caja de texto)
        if audio_file:
            result = whisper_model.transcribe(audio_file)
            original_text = result.get("text", "").strip()
        elif text_input:
            original_text = text_input.strip()
        else:
            return "No se ingreso texto ni audio", "",None
        
        # Para Traducir 
         translated = GoogleTranslator(source='auto', target=target_lang).translate(original_text)