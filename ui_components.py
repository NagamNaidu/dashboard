import streamlit as st

# ------------------ CSS STYLING ------------------
def inject_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4a6fa5;
            --secondary: #166088;
            --accent: #4fc3f7;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
        }
       
        /* Main container styling */
        .main-container {
            background-color: #f5f7fa;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
       
        /* Card styling */
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
       
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
       
        .card-header {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--secondary);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--accent);
        }
       
        .card-metric {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }
       
        .card-metric-label {
            font-size: 0.9rem;
            color: var(--dark);
            opacity: 0.8;
        }
       
        /* Button styling */
        .stButton>button {
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
       
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }
       
        /* Custom tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
       
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 25px;
            border-radius: 8px 8px 0 0 !important;
            background-color: #e9ecef !important;
            transition: all 0.3s ease !important;
        }
       
        .stTabs [aria-selected="true"] {
            background-color: var(--primary) !important;
            color: white !important;
        }
       
        /* Table styling */
        .stDataFrame {
            border-radius: 10px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
       
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
       
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
       
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 10px;
        }
       
        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary);
        }
       
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
       
        .animate-fade {
            animation: fadeIn 0.6s ease-out forwards;
        }
       
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .card {
                padding: 1rem;
            }
        }
       
        /* Switch between login/signup */
        .auth-switch {
            text-align: center;
            margin-top: 1rem;
            color: var(--secondary);
            cursor: pointer;
            font-weight: 500;
        }
       
        .auth-switch:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

def metric_card(title, value, delta=None, delta_color="normal"):
    """Create a styled metric card"""
    delta_html = ""
    if delta is not None:
        color = "green" if delta_color == "normal" else "red"
        symbol = "↑" if delta_color == "normal" else "↓"
        delta_html = f"""
        <div style="font-size: 0.9rem; color: {color}; margin-top: 0.2rem;">
            {symbol} {delta}
        </div>
        """
   
    return f"""
    <div class="card animate-fade">
        <div class="card-metric-label">{title}</div>
        <div class="card-metric">{value}</div>
        {delta_html}
    </div>
    """

def create_card(title, content, height=None):
    """Create a styled card container"""
    height_style = f"height: {height};" if height else ""
    return f"""
    <div class="card animate-fade" style="{height_style}">
        <div class="card-header">{title}</div>
        {content}
    </div>
    """