from googletrans import Translator
import streamlit as st
from gtts import gTTS
import os
import base64
import tempfile

def translate_text(text, target_language='en'):
    """
    Translates the given text to the target language.
    
    Args:
        text (str): The text to translate
        target_language (str): The language code to translate to
        
    Returns:
        str: The translated text
    """
    if not text or target_language == 'en':
        return text
        
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

def text_to_speech(text, lang='en'):
    """
    Converts text to speech and returns an HTML audio element.
    
    Args:
        text (str): The text to convert to speech
        lang (str): The language code
        
    Returns:
        str: HTML with audio element
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(fp.name)
            with open(fp.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            os.unlink(fp.name)
            
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        audio_html = f'<audio autoplay controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        return audio_html
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return ""

def apply_high_contrast_css():
    """
    Applies high-contrast CSS styling for better accessibility.
    """
    st.markdown("""
    <style>
    .high-contrast {
        color: white !important;
        background-color: black !important;
    }
    .high-contrast-text {
        color: yellow !important;
        font-weight: bold !important;
    }
    .high-contrast-links a {
        color: #00FFFF !important;
        text-decoration: underline !important;
    }
    </style>
    """, unsafe_allow_html=True)

def increase_font_size(size='medium'):
    """
    Increases font size for better readability.
    
    Args:
        size (str): Size level - 'small', 'medium', 'large', 'x-large'
    """
    sizes = {
        'small': '0.9rem',
        'medium': '1rem',
        'large': '1.2rem',
        'x-large': '1.5rem'
    }
    
    font_size = sizes.get(size, '1rem')
    
    st.markdown(f"""
    <style>
    .increased-font {{
        font-size: {font_size} !important;
    }}
    .stMarkdown p {{
        font-size: {font_size} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_accessibility_sidebar():
    """
    Renders accessibility controls in the sidebar.
    """
    with st.sidebar.expander("Accessibility Options"):
        st.session_state.accessibility['language'] = st.selectbox(
            "Language",
            options=['en', 'es', 'fr', 'de', 'zh-cn', 'ja', 'ko', 'ru', 'ar', 'hi'],
            format_func=lambda x: {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 
                'de': 'German', 'zh-cn': 'Chinese', 'ja': 'Japanese',
                'ko': 'Korean', 'ru': 'Russian', 'ar': 'Arabic', 'hi': 'Hindi'
            }.get(x, x),
            index=0
        )
        
        st.session_state.accessibility['text_to_speech'] = st.checkbox(
            "Enable Text-to-Speech",
            value=st.session_state.accessibility.get('text_to_speech', False)
        )
        
        st.session_state.accessibility['high_contrast'] = st.checkbox(
            "High Contrast Mode",
            value=st.session_state.accessibility.get('high_contrast', False)
        )
        
        st.session_state.accessibility['font_size'] = st.select_slider(
            "Font Size",
            options=['small', 'medium', 'large', 'x-large'],
            value=st.session_state.accessibility.get('font_size', 'medium')
        )
        
    # Apply selected accessibility features
    if st.session_state.accessibility.get('high_contrast', False):
        apply_high_contrast_css()
        
    increase_font_size(st.session_state.accessibility.get('font_size', 'medium'))
    
    return st.session_state.accessibility