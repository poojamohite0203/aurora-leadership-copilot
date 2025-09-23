import streamlit as st

def render_sidebar():
    """Render a styled sidebar with navigation"""
    
    # Custom CSS for sidebar styling
    st.markdown("""
    <style>
    /* Hide default Streamlit page navigation (the radio buttons at top) */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hide any radio button navigation */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] {
        display: none !important;
    }
    
    /* Streamlit sidebar background override */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%) !important;
        color: white !important;
    }
    
    /* Custom sidebar title */
    .sidebar-brand {
        font-size: 1.4rem;
        font-weight: bold;
        letter-spacing: 2px;
        color: #ffffff;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid rgba(255,255,255,0.2);
        background: rgba(0,0,0,0.1);
        border-radius: 8px;
    }
    
    /* Navigation section header */
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Style custom buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        margin: 0.2rem 0 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: translateX(3px) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Footer styling */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3) !important;
        margin: 1.5rem 0 !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: white !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar title (move Aurora AI Leadership Copilot to the very top, larger)
    st.sidebar.markdown('<div class="sidebar-brand" style="font-size:1.2rem; margin-bottom:0.5rem;">Aurora AI Leadership Copilot</div>', unsafe_allow_html=True)
    
    # Dashboard link
    if st.sidebar.button("🏠 DASHBOARD", key="nav_dashboard", use_container_width=True):
        st.switch_page("app.py")
    
    # Create styled navigation options
    nav_options = [
        ("📊 STATUS REPORT", "pages/status_report.py"),
        ("📅 MEETING", "pages/meetings.py"),
        ("📋 CLIP", "pages/clips.py"),
        ("📔 JOURNAL", "pages/journals.py"),
        ("✅ ACTION TRACKER", "pages/action_tracker.py"),
        ("⛔ BLOCKER", "pages/blockers.py"),
        ("🗳 DECISION", "pages/decisions.py"),
        ("🔍 SEARCH", "pages/search.py"),
        ("🤖 ASK", "pages/ask_assistant.py"),
    ]
    
    for label, page in nav_options:
        if st.sidebar.button(label, key=f"nav_{page}", use_container_width=True):
            st.switch_page(page)
