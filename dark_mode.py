import streamlit as st

def apply_dark_mode():
    """Apply dark mode CSS"""
    dark_css = """
    <style>
    :root {
        color-scheme: dark;
    }
    
    .stApp {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    .stMarkdown, .stText, .stWritten {
        color: #e0e0e0 !important;
    }
    
    .stMetric {
        background-color: #2d2d2d !important;
        border-color: #667eea !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d2d2d;
        border-color: #667eea;
    }
    
    .stDataFrame {
        background-color: #2d2d2d !important;
    }
    
    .stSelectbox, .stTextInput, .stTextArea {
        background-color: #2d2d2d !important;
        color: #e0e0e0 !important;
    }
    
    .stInfo, .stSuccess, .stWarning, .stError {
        background-color: #2d2d2d !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    </style>
    """
    return dark_css

def apply_light_mode():
    """Apply light mode CSS (default)"""
    light_css = """
    <style>
    :root {
        color-scheme: light;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    </style>
    """
    return light_css

def toggle_dark_mode():
    """Toggle dark mode in sidebar"""
    
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    st.session_state.dark_mode = st.sidebar.toggle("🌙 Dark Mode", st.session_state.dark_mode)
    
    if st.session_state.dark_mode:
        st.markdown(apply_dark_mode(), unsafe_allow_html=True)
    else:
        st.markdown(apply_light_mode(), unsafe_allow_html=True)
    
    return st.session_state.dark_mode
