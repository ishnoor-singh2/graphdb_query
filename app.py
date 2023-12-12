import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
# Import utility functions from your modules
from utils import load_config, process_query,process_and_upload_csv
from ui_helper import display_chat_history, handle_about

# Load configurations
config = load_config('config.json')

# Streamlit Page Configuration
st.set_page_config(
    page_title="Natural Language Interface to Clinical Trial Data",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Main Menu", ["ABOUT", "Upload Data", "Model Interface", 'SETTINGS'],
                           icons=['house', 'cloud-upload', 'chat-left-text', 'gear'], menu_icon="cast", default_index=0)

# Handle Sidebar Options
if selected == "ABOUT":
    handle_about()
elif selected == "Model Interface":
    # Model Interface Page
    st.title("Query Clinical Trial Data")

    # Session State Initialization
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = []
    if "model_response" not in st.session_state:
        st.session_state["model_response"] = []

    # User Input for Queries
    query = st.text_input("")

    # Query Processing
    if query:
        with st.spinner(text='In progress'):
            try:
                response = process_query(query)
                st.session_state["user_input"].append(query)
                st.session_state["model_response"].append(response)
                st.success('Query processed successfully')
            except Exception as e:
                st.error(f"An error occurred: {e}")


    # Display Chat History
    display_chat_history(st.session_state["user_input"], st.session_state["model_response"])
elif selected == "Upload Data":
    # Data Upload Page
    st.title("Upload Clinical Trial Data")

    # File Uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        # Process the file
        try:
            data_df = pd.read_csv(uploaded_file)
            json_data = process_and_upload_csv(data_df, config['neo4j'])
            st.success('File processed and data uploaded successfully')
            st.json(json_data)  # Displaying the JSON data
        except Exception as e:
            st.error(f"An error occurred: {e}")
elif selected == "SETTINGS":
    st.write("Settings and configurations will be implemented here.")
