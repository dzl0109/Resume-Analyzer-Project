from fpdf import FPDF
import base64
from io import BytesIO

def generate_pdf_report(analysis_text):
    """Generate professional PDF report from analysis."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add analysis content
    pdf.multi_cell(0, 10, analysis_text)
    
    # Save to bytes buffer
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    
    return buffer.getvalue()