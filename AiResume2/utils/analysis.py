import google.generativeai as genai
import os

def analyze_resume_with_gemini(resume_text, job_description=None):
    """Analyze resume content using Gemini API."""
    
    model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    
    if job_description:
        prompt = f"""
        You are an expert resume reviewer and career coach. Please analyze the following resume in relation to the provided job description.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please provide detailed and constructive feedback on the following aspects:
        1. Overall structure and formatting
        2. Content relevance to the job description
        3. Skills match and gaps
        4. Experience and achievements presentation
        5. ATS compatibility
        6. Key strengths of the resume
        7. Suggested improvements with specific examples
        
        Format your response in a clear, organized manner with separate sections for each aspect.
        """
    else:
        prompt = f"""
        You are an expert resume reviewer and career coach. Please analyze the following resume:

        {resume_text}

        Please provide detailed and constructive feedback on the following aspects:
        1. Overall structure and formatting
        2. Content quality and impact
        3. Skills presentation
        4. Experience and achievements clarity
        5. ATS compatibility
        6. Key strengths of the resume
        7. Suggested improvements with specific examples
        
        Format your response in a clear, organized manner with separate sections for each aspect.
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error occurred while analyzing resume: {str(e)}"