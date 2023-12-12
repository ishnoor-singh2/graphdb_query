# Clinical Trials Knowledge Graph Interface

## Project Overview
This project aims to enhance the discovery and analysis of clinical trial data using a graph database and natural language processing. It utilizes Neo4j for data storage and OpenAI's LLM for query processing, integrated through the LangChain framework.

## Project Structure
- `app.py`: The main Streamlit application file for the web interface.
- `utils.py`: Contains utility functions for loading configurations and processing queries.
- `ui_helpers.py`: Includes functions for handling the UI components like chat history and sidebar content.
- `get_prompt.py`: Provides a template for generating LangChain prompts.
- `gpt_main.py`: Establishes the connection between the model, graph, and LangChain.
- `config.json`: Configuration file to store API keys and database credentials.

## Running
1. Install the requirements
2. Run using streamlit run app.py
3. ensure all the helper scripts are under the app.py directory
