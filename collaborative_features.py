import pandas as pd
import streamlit as st
import json
import os
from datetime import datetime

SESSIONS_DIR = "saved_sessions"

def ensure_sessions_dir():
    """Ensure sessions directory exists"""
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)

def save_session(df: pd.DataFrame, session_name: str, analysis_notes: str = ""):
    """Save analysis session"""
    ensure_sessions_dir()
    
    session_data = {
        'name': session_name,
        'timestamp': datetime.now().isoformat(),
        'rows': len(df),
        'columns': len(df.columns),
        'columns_list': df.columns.tolist(),
        'notes': analysis_notes,
        'dtypes': {col: str(df[col].dtype) for col in df.columns}
    }
    
    session_file = f"{SESSIONS_DIR}/{session_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    return session_file

def load_saved_sessions():
    """Load list of saved sessions"""
    ensure_sessions_dir()
    
    sessions = []
    for file in os.listdir(SESSIONS_DIR):
        if file.endswith('.json'):
            with open(f"{SESSIONS_DIR}/{file}", 'r') as f:
                try:
                    session = json.load(f)
                    sessions.append((file, session))
                except:
                    pass
    
    return sorted(sessions, key=lambda x: x[1]['timestamp'], reverse=True)

def share_session_link(session_name: str):
    """Generate shareable session link"""
    # This is a placeholder for actual sharing functionality
    share_link = f"https://datawizard.app/?session={session_name}"
    return share_link

def collaborative_features_ui(df: pd.DataFrame):
    """Main collaborative features UI"""
    st.markdown("## 👥 Collaborative Features")
    
    tab1, tab2 = st.tabs(["Save Session", "Load Session"])
    
    with tab1:
        st.markdown("### 💾 Save Current Analysis")
        
        session_name = st.text_input("Session name", f"analysis_{datetime.now().strftime('%Y%m%d')}")
        notes = st.text_area("Analysis notes", placeholder="Describe your analysis findings...")
        
        if st.button("Save Session"):
            try:
                session_file = save_session(df, session_name, notes)
                st.success(f"✅ Session saved: {session_file}")
                
                st.markdown("### 📤 Share This Session")
                share_link = share_session_link(session_name)
                st.code(share_link)
                st.info("Share this link with colleagues to collaborate")
            except Exception as e:
                st.error(f"Error saving session: {str(e)}")
    
    with tab2:
        st.markdown("### 📂 Load Saved Sessions")
        
        sessions = load_saved_sessions()
        
        if sessions:
            for file, session in sessions:
                with st.expander(f"📋 {session['name']} - {session['timestamp'][:10]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rows", session['rows'])
                    with col2:
                        st.metric("Columns", session['columns'])
                    
                    st.write(f"**Notes:** {session['notes'] or 'No notes'}")
                    st.write(f"**Columns:** {', '.join(session['columns_list'][:5])}...")
                    
                    if st.button(f"View {session['name']}", key=file):
                        st.info("Click the download button above to get the data file")
        else:
            st.info("No saved sessions yet. Save your first analysis!")
