import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Initialize MarkItDown engine
# Note: MarkItDown handles Word, Excel, PPT, PDF, and HTML natively.
md = MarkItDown()

def convert_file(uploaded_file):
    """Processes the uploaded file and returns markdown string."""
    try:
        # MarkItDown can take a file-like object or a path. 
        # For Streamlit, we pass the uploaded file object.
        result = md.convert(uploaded_file)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None

# --- UI Layout ---
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

st.title("📄 Universal Document Reader")
st.markdown("Convert your Office docs, PDFs, and HTML files into clean **Markdown** or **Plain Text** instantly.")

# [2] Upload Area (Supports multiple files)
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            content = convert_file(uploaded_file)
            
            if content:
                # Get the original filename without extension
                base_name = os.path.splitext(uploaded_file.name)[0]
                
                # [2] Instant Preview
                with st.expander(f"👁️ Preview: {uploaded_file.name}", expanded=True):
                    st.text_area(
                        label="Converted Content",
                        value=content,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )
                    
                    # Layout for Download buttons
                    col1, col2 = st.columns(2)
                    
                    # [4] Download as Markdown
                    with col1:
                        st.download_button(
                            label="📥 Download as .md",
                            data=content,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{uploaded_file.name}"
                        )
                    
                    # [4] Download as Text
                    with col2:
                        st.download_button(
                            label="📥 Download as .txt",
                            data=content,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{uploaded_file.name}"
                        )

st.divider()
st.caption("Built with MarkItDown & Streamlit")
