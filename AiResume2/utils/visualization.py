import plotly.express as px
import pandas as pd
import nltk
from nltk.corpus import stopwords

def create_skills_match_chart(matched, missing):
    """Create interactive skills matching visualization."""
    df = pd.DataFrame({
        "Skill": matched + missing,
        "Status": ["Matched"]*len(matched) + ["Missing"]*len(missing)
    })
    
    fig = px.bar(
        df, 
        x="Status", 
        color="Status",
        title="Skills Match Analysis",
        color_discrete_map={"Matched": "#2ecc71", "Missing": "#e74c3c"}
    )
    
    return fig