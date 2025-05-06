import os
import base64
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# API configuratie - prioriteit aan secrets (cloud), anders .env (local)
if 'api' in st.secrets:
    API_KEY = st.secrets['api']['key']
    API_URL = st.secrets['api']['url']
else:
    API_KEY = os.getenv("PRIVATEAI_KEY", "57271f9a4cdf47ada3b3848942be0fd9")
    API_URL = os.getenv("PRIVATEAI_URL", "https://api.private-ai.com/community/v4")

HEADERS = {"x-api-key": API_KEY}

# Sensible huisstijl
SENSIBLE_GREEN = "#016B5B"
SENSIBLE_BLACK = "#212121"
SENSIBLE_GRAY = "#F5F5F5"

# Page configuration
st.set_page_config(
    page_title="Sensible Mask - PDF Protection",
    page_icon="🔒",
    layout="centered",
)

# Custom CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: white;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {SENSIBLE_BLACK};
        font-family: 'Helvetica', sans-serif;
    }}
    .stButton>button {{
        background-color: {SENSIBLE_GREEN};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
    }}
    .stButton>button:hover {{
        background-color: {SENSIBLE_GREEN};
        color: white;
        opacity: 0.9;
    }}
    .stDownloadButton>button {{
        background-color: {SENSIBLE_GREEN};
        color: white;
        border: none;
        border-radius: 4px;
    }}
    .main .block-container {{
        padding-top: 2rem;
    }}
    footer {{
        visibility: hidden;
    }}
    .feature-card {{
        padding: 20px;
        border-radius: 8px;
        background-color: {SENSIBLE_GRAY};
        margin-bottom: 15px;
    }}
    .step-container {{
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }}
    .step-number {{
        background-color: {SENSIBLE_GREEN};
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
        font-weight: bold;
    }}
    .step-text {{
        flex: 1;
    }}
    .intro-text {{
        font-size: 1.1rem;
        margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

def sensible_logo():
    return st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: #016B5B; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; border-radius: 5px; margin-right: 10px;">
            <span style="color: white; font-weight: bold; font-size: 24px;">S</span>
        </div>
        <span style="font-size: 24px; font-weight: bold; color: #212121;">Sensible Mask</span>
    </div>
    """, unsafe_allow_html=True)

def feature_card(icon, title, description):
    return st.markdown(f"""
    <div class="feature-card">
        <div style="font-size: 24px; margin-bottom: 10px;">{icon}</div>
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 5px;">{title}</div>
        <div style="color: #666;">{description}</div>
    </div>
    """, unsafe_allow_html=True)

def step(number, text):
    return st.markdown(f"""
    <div class="step-container">
        <div class="step-number">{number}</div>
        <div class="step-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Application header
    sensible_logo()
    st.subheader("Mask sensitive information in PDF documents")
    
    # Introduction
    st.markdown("""
    <div class="intro-text">
    Sensible Mask automatically detects and redacts sensitive information in your PDF documents. 
    Protect personal data, confidential information, and comply with privacy regulations with just a few clicks.
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.write("### Why choose Sensible Mask?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        feature_card("🔒", "Privacy First", "Built with privacy in mind to keep your sensitive data secure.")
        feature_card("⚡", "Fast Processing", "Get your redacted documents in seconds, not minutes.")
    
    with col2:
        feature_card("🤖", "AI-Powered", "Advanced AI identifies personal information with high accuracy.")
        feature_card("🔍", "Easy to Use", "Simple interface that anyone can use without training.")
    
    # How it works
    st.write("### How it works")
    
    step(1, "Upload your PDF document")
    step(2, "Our AI identifies and marks sensitive information")
    step(3, "Review and download your redacted document")
    
    st.divider()
    
    # Upload section
    st.write("### Try it now")
    
    # API key warning if not set
    if not API_KEY:
        st.warning("⚠️ No API key found. Please contact the administrator.")
        st.stop()
    
    # File uploader
    file = st.file_uploader("Upload a PDF", type=["pdf"])
    
    if file:
        # Check file size
        if file.size > 10 * 1024 * 1024:
            st.error("File > 10 MB - please reduce file size or choose another document.")
            st.stop()
        
        # Process button
        if st.button("Redact Document"):
            # Convert file to base64
            data_b64 = base64.b64encode(file.getvalue()).decode()
            payload = {"file": {"data": data_b64, "content_type": "application/pdf"}}
            
            with st.spinner("Masking in progress..."):
                r = requests.post(f"{API_URL}/process/files/base64", json=payload, headers=HEADERS, timeout=120)
            
            if r.ok:
                red_b64 = r.json()["processed_file"]
                red_pdf = base64.b64decode(red_b64)
                st.success("PDF successfully masked! Download below.")
                st.download_button("Download masked PDF", red_pdf, file_name=f"redacted_{file.name}")
                
                # Toon PDF via base64 in een iframe
                base64_pdf = base64.b64encode(red_pdf).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.error(f"API error: {r.status_code} – {r.text}")
    
    # Footer information
    st.divider()
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>Sensible Share With Confidence</div>
        <div style="color: #666; font-size: 0.8rem;">© 2024 Sensible | <a href="#" style="color: #666; text-decoration: none;">Privacy Policy</a> | <a href="#" style="color: #666; text-decoration: none;">Terms of Service</a></div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 