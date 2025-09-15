import streamlit as st

def render_sidebar():
    """Render a styled sidebar with navigation"""
    
    # Custom CSS for sidebar styling
    st.markdown("""
    <style>
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
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
    }
    
    /* Navigation items styling */
    .nav-item {
        padding: 0.7rem 1rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: rgba(255,255,255,0.2);
        border-left: 4px solid #fbbf24;
    }
    
    /* Icon styling */
    .nav-icon {
        font-size: 1.2rem;
        width: 24px;
        text-align: center;
    }
    
    /* Streamlit sidebar background override */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
    }
    
    /* Sidebar text color override */
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar title
    st.sidebar.markdown('<div class="sidebar-brand">🦄 AURORA COPILOT</div>', unsafe_allow_html=True)
    
    # Navigation menu
    st.sidebar.markdown("### 📍 NAVIGATION")
    
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
    
    # Add some footer info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🚀 Aurora AI Leadership Copilot**")
    st.sidebar.markdown("*Intelligent productivity insights*")
