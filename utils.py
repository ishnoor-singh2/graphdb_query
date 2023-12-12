import json
from langchain.graphs import Neo4jGraph
from langchain.chat_models import ChatOpenAI
from get_prompt import generate_prompt_template
from gpt_main import get_gpt_chain

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

def init_graph_and_model(neo4j_config, llm_config):
    """Initialize Neo4j graph and language model."""
    graph = Neo4jGraph(**neo4j_config)
    model = ChatOpenAI(**llm_config)
    return graph, model

def process_query(query):
    """Process a user query and return the model's response."""
    try:
        # Load configurations
        config = load_config('config.json')  # Assuming the config file is named 'config.json'

        graph , model = init_graph_and_model(config['neo4j'],config['llm_openai'])

        # Initialize the graph and refresh its schema
        # graph = Neo4jGraph(**config['neo4j'])
        graph.refresh_schema()

        # Initialize the language model
        # model = ChatOpenAI(**config['llm_openai'])

        # Generate the Langchain prompt template
        langchain_prompt_template = generate_prompt_template()

        # Get the GPT chain
        gpt_call = get_gpt_chain(model, graph, langchain_prompt_template)

        # Run the query and return the response
        return gpt_call.run(query)

    except Exception as e:
        raise e  # Rethrow the exception to be handled by the caller

def process_and_upload_csv(df, neo4j_config):
    """
    Process the uploaded CSV data and upload it to Neo4j.
    Returns the processed data in JSON format.
    """
        # Load configurations
    config = load_config('config.json')  # Assuming the config file is named 'config.json'

    graph , model = init_graph_and_model(config['neo4j'],config['llm_openai'])
    # Process the DataFrame (df) into the desired format
    # ...

    # Upload to Neo4j
    # You'll need to write the logic to connect to Neo4j and upload the data
    # ...

    # For demonstration, return the processed data as JSON
    return df.to_json(orient='records')
