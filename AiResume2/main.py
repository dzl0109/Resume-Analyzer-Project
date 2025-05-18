import streamlit as st
from utils.file_processing import *
from utils.analysis import *
from utils.visualization import *
from utils.export import *
from utils.accessibility import *
from utils.file_processing import *
#We had chatgbt help us debug and write the code.
def setup_accessibility_features():
    """
    Sets up accessibility features for the application
    including language translation, text-to-speech, and color schemes.
    
    Returns:
        dict: A dictionary containing accessibility settings
    """
    import streamlit as st
    
    # Initialize accessibility settings in session state if not already present
    if 'accessibility' not in st.session_state:
        st.session_state.accessibility = {
            'language': 'en',
            'text_to_speech': False,
            'high_contrast': False,
            'font_size': 'medium'
        }
    
    # Return the current settings
    return st.session_state.accessibility

def setup_language_support():
    """
    Sets up language support for the application.
    
    Returns:
        dict: A dictionary containing language settings
    """
    # Initialize language settings in session state if not already present
    if 'language' not in st.session_state:
        st.session_state.language = {
            'current': 'en',
            'available': ['en', 'es', 'fr', 'de', 'zh-cn', 'ja'],
            'auto_detect': False
        }
    
    # Return the current settings
    return st.session_state.language

def extract_text_from_pdf(pdf_file):
    """Enhanced PDF text extraction with error handling and text cleanup."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # Only add non-empty pages
                text += page_text + "\n\n"
        
        # Basic text cleanup
        text = text.replace('\n\n', '\n').strip()
        return text
    except Exception as e:
        st.error(f"PDF extraction error: {str(e)}")
        return ""

def extract_text_from_docx(docx_file):
    """Enhanced DOCX extraction including tables and formatting."""
    try:
        doc = docx.Document(docx_file)
        full_text = []
        
        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        
        # Extract tables
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    row_text.append(cell.text.strip())
                full_text.append(" | ".join(row_text))
        
        return "\n".join(full_text)
    except Exception as e:
        st.error(f"DOCX extraction error: {str(e)}")
        return ""
    
def display_resume_analysis_page(model_option, analysis_type, accessibility_settings):
    """
    Display the resume analysis page with file upload and results.
    
    Args:
        model_option (str): The selected AI model
        analysis_type (str): The type of analysis to perform
        accessibility_settings (dict): Accessibility settings
    """
    st.header("Resume Analysis")
    st.subheader("Upload your resume for AI-powered analysis")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
    
    # Optional job description
    use_job_description = st.checkbox("Include a job description for targeted feedback")
    job_description = None
    
    if use_job_description:
        job_description = st.text_area("Paste the job description here", height=200)
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        if st.button("Analyze Resume", type="primary"):
            with st.spinner("Analyzing your resume... This may take a moment."):
                try:
                    # Extract text from resume
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    # Display extracted text (optional)
                    with st.expander("Show Extracted Resume Text"):
                        st.text_area("Extracted Text", resume_text, height=300)
                    
                    # Analyze resume with Gemini
                    analysis = analyze_resume_with_gemini(
                        resume_text, 
                        job_description,
                        model=model_option,
                        analysis_type=analysis_type
                    )
                    
                    # Display analysis in tabs
                    st.subheader("Resume Analysis Results")
                    
                    tab1, tab2, tab3 = st.tabs(["Complete Analysis", "Key Strengths", "Improvement Areas"])
                    
                    with tab1:
                        st.markdown(analysis)
                    
                    with tab2:
                        # Extract strengths section (placeholder - implement your own extraction logic)
                        st.markdown("### Key Strengths")
                        st.info("Implement extraction of strengths section from the full analysis")
                    
                    with tab3:
                        # Extract improvement areas (placeholder - implement your own extraction logic)
                        st.markdown("### Suggested Improvements")
                        st.info("Implement extraction of improvement areas from the full analysis")
                    
                    # Download options
                    st.markdown("---")
                    st.subheader("Download Options")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download Analysis as Text",
                            data=analysis,
                            file_name="resume_analysis.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Generate PDF (placeholder - implement your PDF generation)
                        st.download_button(
                            label="Download Analysis as PDF",
                            data=analysis,  # Replace with PDF generation function
                            file_name="resume_analysis.pdf",
                            mime="application/pdf",
                            disabled=True  # Enable after implementing PDF generation
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Try uploading a different file format or check if the file is corrupted.")

def display_skills_matching_page():
    """Display the skills matching page."""
    st.header("Skills Matching")
    st.subheader("Match your skills with job requirements")
    
    # Job description input
    job_description = st.text_area("Paste job description here")
    
    # Upload resume if not already uploaded
    if 'uploaded_file' not in st.session_state:
        uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx", "txt"])
    else:
        st.success(f"Using already uploaded resume: {st.session_state.uploaded_file.name}")
    
    if job_description and ('uploaded_file' in st.session_state or uploaded_file):
        st.button("Match Skills", on_click=lambda: st.info("Skills matching functionality would go here"))

def display_about_page():
    """Display the about page."""
    st.header("About Resume Analyzer Pro")
    
    st.markdown("""
    ## AI-Powered Resume Analysis
    
    Resume Analyzer Pro uses advanced AI models to analyze your resume and provide 
    actionable insights to help improve your job application materials.
    
    ### Features:
    
    - **Comprehensive Analysis**: Get detailed feedback on your resume's content and structure
    - **Skills Matching**: Compare your skills against job descriptions
    - **Improvement Suggestions**: Receive AI-powered suggestions to enhance your resume
    - **Accessibility Options**: Use the app in your preferred language with accessibility features
    
    ### How It Works:
    
    1. Upload your resume
    2. Select analysis options
    3. Review the AI-generated insights
    4. Export your results
    
    ### Privacy:
    
    Your data is processed securely and not stored permanently. All analysis happens within the app.
    """)

def display_settings_page():
    """Display the settings page."""
    st.header("Settings")
    
    # App settings tab
    with st.expander("Application Settings", expanded=True):
        st.checkbox("Dark Mode", key="dark_mode")
        st.checkbox("Save Analysis History", key="save_history")
        st.slider("Result Detail Level", 1, 5, 3, key="detail_level")
    
    # Display accessibility settings from sidebar in main area too
    with st.expander("Accessibility Settings"):
        render_accessibility_sidebar()
    
    # Export settings
    with st.expander("Export Settings"):
        st.checkbox("Include Visualization in Reports", key="include_viz", value=True)
        st.checkbox("Add Improvement Suggestions", key="add_suggestions", value=True)
        export_format = st.selectbox("Default Export Format", ["PDF", "Word", "Plain Text", "HTML"])
        st.session_state.export_format = export_format

def main():
    """Main application entry point with enhanced UI and features."""
    
    # Configure page settings
    st.set_page_config(
        page_title="AI Resume Analyzer Pro", 
        page_icon="📝", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Setup accessibility features
    accessibility_settings = setup_accessibility_features()
    
    # Setup language support
    language_settings = setup_language_support()
    
    # Create sidebar navigation
    with st.sidebar:
        st.title("Resume Analyzer Pro")
        
        # Try to load the logo, but handle the case if it's missing
        try:
            # First try with the original path
            st.image("assets/logo.png", width=150)
        except Exception as e:
            # If that fails, check if we need to create directories
            import os
            
            # Create assets directory if it doesn't exist
            if not os.path.exists("assets"):
                os.makedirs("assets")
                st.warning("Created assets directory. Please add a logo.png file there.")
            else:
                # If the directory exists but the file is missing, show a message
                st.info("Logo image not found. Using text instead.")
                st.markdown("### 📝 Resume AI")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Resume Analysis", "Skills Matching", "About", "Settings"]
        )
        
        # Model selection
        model_option = st.selectbox(
            "Select AI Model",
            ["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-preview-04-17"],
            help="Flash for speed, Pro for deeper analysis"
        )
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Focus",
            ["General", "Technical", "Executive", "Entry-Level", "Career Change"],
            help="Select the type of analysis most relevant to your needs"
        )
    
    # Main content routing
    if page == "Resume Analysis":
        display_resume_analysis_page(model_option, analysis_type, accessibility_settings)
    elif page == "Skills Matching":
        display_skills_matching_page()
    elif page == "About":
        display_about_page()
    elif page == "Settings":
        display_settings_page()

    # Information about API key setup
    with st.expander("How to set up your Google Gemini API key"):
        st.write("""
        1. Go to Google AI Studio: https://makersuite.google.com/app/apikey
        2. Create or sign in to your Google account
        3. Generate an API key
        4. Create a file named `.env` in the same directory as this script
        5. Add the following line to the .env file: `GOOGLE_API_KEY=your_api_key_here`
        6. Restart the application
        """)
    
    # App information footer
    st.markdown("---")
    st.markdown("### About this App")
    st.write("""
    This Resume Analyzer uses Google's Gemini AI to provide professional feedback on your resume.
    The application does not store your resume or job description - all processing is done in memory.
    For best results, use a PDF or DOCX format resume with clean formatting.
    """)

if __name__ == "__main__":
    main()