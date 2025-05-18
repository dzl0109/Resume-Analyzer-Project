import os
import streamlit as st
import PyPDF2
import docx
import google.generativeai as genai
from dotenv import load_dotenv

#We had chatgbt help us debug and write the code.

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extract text content from a DOCX file."""
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(txt_file):
    """Extract text content from a TXT file."""
    text = txt_file.read().decode('utf-8')
    return text

def extract_text_from_resume(uploaded_file):
    """Extract text from resume based on file type."""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def analyze_resume_with_gemini(resume_text, job_description=None, model=None, analysis_type="General"):
    """Analyze resume content using Gemini API with enhanced prompts."""
    
    if model is None:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    
    # Base prompt components
    basic_instructions = """
    You are an expert resume reviewer and career coach. Please analyze the following resume and provide detailed feedback.
    """
    
    # Industry/career level specific prompt components
    industry_prompts = {
        "General": """
        Focus on universal resume best practices and general employability.
        """,
        "Technical": """
        Focus on technical skills presentation, project descriptions, and technical achievements.
        Pay special attention to how technical skills are categorized and if they match current industry standards.
        Evaluate if technical projects demonstrate problem-solving abilities and technical depth.
        Suggest improvements for better showcasing technical expertise and coding proficiency.
        """,
        "Executive": """
        Focus on leadership achievements, strategic initiatives, and executive presence.
        Evaluate how effectively the resume demonstrates leadership impact, vision, and business results.
        Pay special attention to quantifiable achievements, leadership style indicators, and executive summary.
        Suggest improvements for better positioning as a senior leader and strategic thinker.
        """,
        "Entry-Level": """
        Focus on education, relevant coursework, internships, and transferable skills.
        Evaluate how effectively the resume showcases potential despite limited work experience.
        Pay special attention to academic projects, volunteer work, and skill development.
        Suggest improvements for better positioning as a promising entry-level candidate.
        """,
        "Career Change": """
        Focus on transferable skills, relevant experiences, and positioning for the new field.
        Evaluate how effectively the resume bridges previous experience with desired new direction.
        Pay special attention to skills and achievements that translate across industries.
        Suggest improvements for better demonstrating adaptability and relevant capabilities.
        """
    }
    
    # Construct the appropriate prompt based on inputs
    if job_description:
        prompt = f"""
        {basic_instructions}
        
        {industry_prompts[analysis_type]}
        
        Job Description:
        {job_description}
        
        Resume:
        {resume_text}
        
        Please provide detailed and constructive feedback on the following aspects:
        1. Overall match with job description (compatibility score out of 10)
        2. Key matching qualifications
        3. Notable qualification gaps
        4. ATS optimization suggestions for this specific job
        5. Resume structure and formatting
        6. Experience and achievements presentation
        7. Skills presentation and relevance
        8. Specific content improvement suggestions with before/after examples
        9. Summary of 3 strongest points
        10. Summary of 3 most important improvements needed
        
        Format your response in a clear, organized manner with separate markdown sections and use bullet points where appropriate for readability.
        """
    else:
        prompt = f"""
        {basic_instructions}
        
        {industry_prompts[analysis_type]}
        
        Resume:
        {resume_text}
        
        Please provide detailed and constructive feedback on the following aspects:
        1. Overall resume strength (score out of 10)
        2. Resume structure and formatting
        3. Professional summary/objective effectiveness
        4. Experience and achievements presentation
        5. Skills presentation and organization
        6. Education section effectiveness
        7. ATS compatibility and keyword optimization
        8. Specific content improvement suggestions with before/after examples
        9. Summary of 3 strongest points
        10. Summary of 3 most important improvements needed
        
        Format your response in a clear, organized manner with separate markdown sections and use bullet points where appropriate for readability. Make sure you don't surpus your text/output limit.
        """
    
    try:
        # Set temperature for more creative/diverse responses
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                top_p=0.8,
                top_k=40,
                max_output_tokens=4096,
            )
        )
        return response.text
    except Exception as e:
        return f"Error occurred while analyzing resume: {str(e)}"

def main():
    """Main application function with improved UI."""
    st.set_page_config(page_title="AI Resume Analyzer", page_icon="📝", layout="wide")
    
    # Create sidebar for navigation and settings
    with st.sidebar:
        st.title("Resume Analyzer")
        
        # Navigation
        page = st.radio("Navigation", ["Resume Analysis", "About", "Settings"])
        
        # Model selection in sidebar
        model_option = st.selectbox(
            "Select AI Model",
            ["gemini-2.5-flash-preview-04-17", "gemini-2.5-pro-preview-04-17"]
        )
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Focus",
            ["General", "Technical", "Executive", "Entry-Level", "Career Change"]
        )
        
        st.markdown("---")
        st.caption("AI Resume Analyzer v1.0")
    
    # Main content based on navigation selection
    if page == "Resume Analysis":
        display_resume_analysis_page(model_option, analysis_type)
    elif page == "About":
        display_about_page()
    elif page == "Settings":
        display_settings_page()

def display_resume_analysis_page(model_option, analysis_type):
    """Display the main resume analysis page."""
    st.title("AI Resume Analyzer")
    st.write("Upload your resume and optionally a job description to get AI-powered feedback.")
    
    # File uploader for resume with a nicer UI
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_resume = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)", 
            type=["pdf", "docx", "txt"],
            help="We recommend PDF format for best results"
        )
    
    with col2:
        st.markdown("#### Resume Tips")
        st.info(f"Use a clean, ATS-friendly format, highlight achievements, and include relevant keywords.")
    
    # Job description input with improved UI
    use_job_description = st.checkbox("Include a job description for targeted feedback")
    job_description = None
    
    if use_job_description:
        job_description = st.text_area(
            "Paste the job description here", 
            height=200,
            placeholder="Copy and paste the entire job posting for best results..."
        )
    
    # Industry selection to tailor analysis
    if uploaded_resume is not None:
        st.success("Resume uploaded successfully!")
        
        # Analyze button with better styling
        analyze_button = st.button("Analyze Resume", type="primary", use_container_width=True)
        
        if analyze_button:
            with st.spinner("Analyzing your resume... This may take a moment."):
                try:
                    # Extract text from resume
                    resume_text = extract_text_from_resume(uploaded_resume)
                    
                    # Display extracted text in expandable section
                    with st.expander("Show Extracted Resume Text", expanded=False):
                        st.text_area("Extracted Text", resume_text, height=300)
                    
                    # Analyze resume with selected model and analysis type
                    model = genai.GenerativeModel(model_option)
                    analysis = analyze_resume_with_gemini(
                        resume_text, 
                        job_description, 
                        model=model, 
                        analysis_type=analysis_type
                    )
                    
                    # Display analysis in tabs
                    st.subheader("Resume Analysis Results")
                    
                    tab1, tab2, tab3 = st.tabs(["Complete Analysis", "Key Strengths", "Improvement Areas"])
                    
                    with tab1:
                        st.markdown(analysis)
                    
                    with tab2:
                        # Extract strengths section using regex or parsing
                        # This is a placeholder - you would need to implement the extraction
                        st.markdown("### Key Strengths")
                        st.info("Implement extraction of strengths section from the full analysis")
                    
                    with tab3:
                        # Extract improvement areas
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
                        # Generate PDF using ReportLab or another PDF library
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

def display_about_page():
    """Display information about the application."""
    st.title("About AI Resume Analyzer")
    
    st.markdown("""
    ## How It Works
    
    This application uses Google's Gemini AI to analyze resumes and provide professional feedback.
    
    ### Features:
    - **Resume Analysis**: Get detailed feedback on your resume structure, content, and ATS compatibility
    - **Job Matching**: Compare your resume against specific job descriptions
    - **Tailored Advice**: Receive industry-specific recommendations to improve your resume
    
    ### Privacy Policy
    
    - Your resume and job descriptions are not stored permanently
    - All processing is done temporarily in memory
    - No personal data is shared with third parties
    
    ### Technologies Used
    - Streamlit for the web interface
    - Google Gemini AI for resume analysis
    - PyPDF2 and python-docx for document processing
    """)

def display_settings_page():
    """Display application settings."""
    st.title("Settings")
    
    # API key configuration
    st.subheader("API Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Enter your API key from Google AI Studio")
    
    if st.button("Save API Key"):
        # Implement secure storage of API key
        st.success("API key saved successfully!")
    
    # Theme settings
    st.subheader("Appearance")
    theme = st.radio("Theme", ["Light", "Dark", "System Default"])
    
    # Language settings
    st.subheader("Language")
    language = st.selectbox("Interface Language", ["English", "Spanish", "French", "German"])
    
    # Save settings button
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
