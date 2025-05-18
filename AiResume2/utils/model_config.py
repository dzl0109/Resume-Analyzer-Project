import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class ModelConfigurator:
    """Handles AI model selection and configuration."""
    
    @staticmethod
    def setup_controls():
        """
        Create Streamlit UI controls for model configuration.
        
        Returns:
            dict: Configuration settings including:
                - model: Selected model name
                - temperature: Creativity control
                - max_tokens: Output length
                - safety_level: Content filtering
        """
        with st.sidebar.expander("AI Settings"):
            # Model selection dropdown
            model = st.selectbox(
                "Model Version",
                options=["gemini-flash", "gemini-pro"],
                help="Flash for speed, Pro for deeper analysis"
            )
            
            # Creativity slider
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1
            )
            
            # Output length control
            detail_level = st.select_slider(
                "Detail Level",
                options=["Brief", "Standard", "Detailed"],
                value="Standard"
            )
            
            # Map detail level to token count
            token_map = {
                "Brief": 1024,
                "Standard": 2048,
                "Detailed": 4096
            }
            
            # Safety settings
            safety_level = st.select_slider(
                "Content Filter",
                options=["Minimal", "Moderate", "Strict"],
                value="Moderate"
            )
            
        return {
            "model": f"gemini-1.5-{model}-latest",
            "temperature": temperature,
            "max_tokens": token_map[detail_level],
            "safety_level": safety_level
        }

    @staticmethod
    def configure_model(settings):
        """
        Initialize Gemini model with specified settings.
        
        Args:
            settings (dict): Configuration from setup_controls()
            
        Returns:
            GenerativeModel: Configured AI model instance
        """
        # Map safety levels to Gemini thresholds
        safety_map = {
            "Minimal": HarmBlockThreshold.BLOCK_ONLY_HIGH,
            "Moderate": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            "Strict": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
        }
        
        # Configure generation parameters
        generation_config = {
            "temperature": settings["temperature"],
            "max_output_tokens": settings["max_tokens"]
        }
        
        # Configure safety settings
        safety_settings = {
            category: safety_map[settings["safety_level"]]
            for category in [
                HarmCategory.HARM_CATEGORY_HARASSMENT,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT
            ]
        }
        
        return genai.GenerativeModel(
            model_name=settings["model"],
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    @staticmethod
    def customize_prompt(base_prompt, config):
        """
        Enhance prompt based on user preferences.
        
        Args:
            base_prompt (str): Standard prompt template
            config (dict): User configuration
            
        Returns:
            str: Enhanced prompt with specific instructions
        """
        # Add detail level instructions
        if config["max_tokens"] <= 1024:
            base_prompt += "\n\nPlease provide concise bullet points."
        elif config["max_tokens"] >= 4096:
            base_prompt += "\n\nInclude detailed examples and explanations."
            
        # Add creativity instructions
        if config["temperature"] > 0.7:
            base_prompt += "\n\nProvide creative suggestions."
            
        return base_prompt