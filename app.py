import streamlit as st
import os
import zipfile
from markitdown import MarkItDown
from io import BytesIO

# Initialize MarkItDown engine
md = MarkItDown()

def format_size(bytes_size):
    """Converts bytes to a human-readable string (MB)."""
    return f"{bytes_size / (1024 * 1024):.4f} MB"

def process_file_content(file_obj, filename):
    """Core conversion logic with error handling and stable processing."""
    try:
        # markitdown processes the file object directly
        result = md.convert(file_obj)
        return result.text_content
    except Exception:
        st.error(f"⚠️ Could not read {filename}. Please check if the format is supported or corrupted.")
        return None

def display_file_ui(content, original_size, filename):
    """Renders the Tabbed UI for each successfully processed file."""
    base_name = os.path.splitext(filename)[0]
    converted_bytes = len(content.encode('utf-8'))
    
    # Create Tabs for Preview and Analytics
    tab_preview, tab_stats = st.tabs(["📝 Text Preview", "📊 File Size Comparison"])
    
    with tab_preview:
        st.text_area("Markdown Content", content, height=300, key=f"preview_{filename}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download .md",
                data=content,
                file_name=f"{base_name}_converted.md",
                mime="text/markdown",
                key=f"dl_md_{filename}"
            )
        with col2:
            st.download_button(
                label="📥 Download .txt",
                data=content,
                file_name=f"{base_name}_converted.txt",
                mime="text/plain",
                key=f"dl_txt_{filename}"
            )

    with tab_stats:
        # Comparison Table
        st.table({
            "File Version": ["Original File", "Converted Text"],
            "Size (MB)": [format_size(original_size), format_size(converted_bytes)]
        })
        
        # Percentage Calculation
        if original_size > 0:
            reduction = ((original_size - converted_bytes) / original_size) * 100
            if reduction > 0:
                st.success(f"✅ Text version is **{reduction:.1f}% smaller** than the original.")
            else:
                st.info("Note: The text output is slightly larger than the source (common for small/highly compressed files).")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📑", layout="wide")

st.title("📑 Universal Document-to-Text")
st.markdown("Upload **Word, Excel, PPT, PDF, HTML, or ZIP** files to extract clean Markdown text.")

# [Requirement 2] Upload Area
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
