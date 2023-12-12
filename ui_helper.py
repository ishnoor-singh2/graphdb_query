import streamlit as st

def display_chat_history(user_inputs, model_responses):
    """Display the conversation history."""
    for user_input, model_response in zip(user_inputs, model_responses):
        with st.container():
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                st.write(model_response)

def handle_about():
    """Handle the display of information in the sidebar."""
    st.title("About This App")
    st.markdown(
        """
        ### Natural Language Interface to Clinical Trial Data
        #### By Ishnoor Singh (M22AIE233) , Nikita Pise ( M22AIE244 ) , Sourav Ghosh (M22 xxxxx)
        This application provides an easy-to-use interface for querying clinical trial data using natural language. 
        It's designed to help researchers, medical professionals, and anyone interested in clinical trials 
        to quickly find relevant information without the need for complex database queries.

        ### Key Features
        - **Natural Language Queries**: Simply type your questions in everyday language.
        - **Data Upload**: Upload clinical trial data in CSV format.
        - **Real-time Processing**: Immediate responses to your queries.
        - **Neo4j Integration**: Data is stored and managed in a Neo4j graph database.

        ### Sample Questions
        You can ask questions like:
        - "List the trial id of trials studying Hematologic Malignancy and give their URLs."
        - "Show trials conducted in Germany for diabetes."
        - "What are the latest trials for COVID-19 vaccines?"
        - "Provide a summary of the trial NCT123456789."
        - "Which trials are currently in Phase 3 and involve immunotherapy?"

        _Note: This application is for informational purposes and should not replace professional medical advice._

        ### Getting Started
        To start, select an option from the menu. You can upload data, make queries.
        """
    )




    """
            ## Example questions

        * List the trial id of trial studying Hematologic Malignancy disease and give its url?
        * List the titles of the trials in China?
        * I have a patient having Borderline Personality Disorder, 
          suggest some trial studying Borderline Personality Disorder, give me its brief summary in a line?
        * List the title of all trials happening in Switzerland.
        * Show the top trial based on studyStartDate studying Overweight and Obesity, give the trial's url?
        * I have a patient having Parkinson's Disease, suggest some trial studying Parkinson's Disease?
        * Explain in short about the trial studying Arrythmia and give its URL?

    """

