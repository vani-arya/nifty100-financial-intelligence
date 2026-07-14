import streamlit as st
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Analytics")

st.success(
    "Welcome to the Nifty 100 Financial Intelligence Platform"
)

st.markdown(
    """
    Use the sidebar to navigate
    through all dashboard screens.
    """
)