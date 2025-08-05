#Wilbel Benitez
#22-SISN-2-064
import gradio as gr
import whisper
from deep_translator import GoogleTranslator 
from gtts import gTTS
import tempfile
import os

# Cargamos el modelo Whisper (Tiny este es el mas liviano)
whisper_model = whisper.load_model("tiny")

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
        
        #Convertir texto traducido a audio con gTTS
        tts = gTTS(text=translated, lang=target_lang)

        #Guardar audio como archivo temporal 
        temp_file = tempfile.NamedTemporaryFile(suffix= "mp3", delete=False)
        tts_path = temp_file.name 
        tts.save(tts_path)

        return original_text, translated, tts_path
    except Exception as e:
        return f"Error:{str(e)}","", None
    
#interfaz Gradio 
iface = gr.Interface(
    fn=translate_input,
    inputs=[
        gr.Audio(type="filepath", label= " 🎙️ Audio (opcional)"),
        gr.Textbox(label="📝 Texto (opcional)"),
        gr.Dropdown(choices=["es", "en", "fr", "de", "it", "pt"], label="🌍 Idioma de destino", value="es"),

    ],
    outputs=[
        gr.Textbox(label="🗣️ Texto original detectado o ingresado"),
        gr.Textbox(label="🌍 Traducción"),
        gr.Audio(label="🔊 Audio traducido")
    ],
    title="🌐 Traductor Ligero de Voz o Texto",
    description="Traduce voz o texto fácilmente y escúchalo en el idioma de destino. No necesita GPU ni paquetes pesados."
)

iface.launch()
 
