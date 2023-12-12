import json
import pandas as pd
import numpy as np
file_path = r'Data/merged_output.csv'

# Create an instance of the loader
json_path = r'config.json'
with open(json_path) as config_json:
    config = json.load(config_json)

from neo4j import GraphDatabase
uri = "neo4j+s://cf1b9b39.databases.neo4j.io" 
driver = GraphDatabase.driver(uri , auth = ("neo4j","vRDqUrdllXu6SkFA8vtxBk1bppbYHA-NFZc1mhjtgxY"))

def preprocess(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.lower()
        df[col] = df[col].fillna('')
    return df

def load_data_to_neo4j(data):
    with driver.session() as session:
        # Load Trial data
        trial_data = data["Trial"]
        # Ensure to use 'TrialID' consistently
        trial_node = session.run("""
            MERGE (t:Trial {TrialID: $TrialID})
            ON CREATE SET t += {
                Title: $trial_data['Title'],
                URL: $trial_data['URL'],
                Status: $trial_data['Status'],
                BriefSummary: $trial_data['Brief Summary'],
                Phase: $trial_data['Phase'],
                StudyStartDate: $trial_data['Study Start Date'],
                ExpectedCompletionDate: $trial_data['Expected Completion Date']
            }
            RETURN t
        """, TrialID=trial_data['Trial ID'], trial_data=trial_data).single()["t"]

        # Load Intervention data and connect to Trial
        interventions = data["Drug/Intervention"]
        for intervention_type, intervention_list in interventions.items():
            for intervention_name in intervention_list:
                intervention_node = session.run("""
                    MERGE (i:Intervention {Name: $Name, Type: $Type})
                    RETURN i
                """, Name=intervention_name, Type=intervention_type).single()["i"]
                session.run("""
                    MATCH (t:Trial {TrialID: $TrialID}), (i:Intervention {Name: $Name, Type: $Type})
                    MERGE (t)-[:USES]->(i)
                """, TrialID=trial_data['Trial ID'], Name=intervention_name, Type=intervention_type)

        # Load Disease/Condition data and connect to Trial
        for disease_name in data["Disease/Condition"]["Disease Name"]:
            disease_node = session.run("""
                MERGE (d:Disease {Name: $Name})
                RETURN d
            """, Name=disease_name).single()["d"]
            session.run("""
                MATCH (t:Trial {TrialID: $TrialID}), (d:Disease {Name: $Name})
                MERGE (t)-[:TARGETS]->(d)
            """, TrialID=trial_data['Trial ID'], Name=disease_name)
                    
        for location in data["Locations"]:
            # Check if at least one attribute is present
            if any(location.get(attr) for attr in ["Institution", "City", "Country"]):
                # Assign default values if 'City', 'Country', or 'Institution' are null
                city = location.get("City", "Unknown")
                country = location.get("Country", "Unknown")
                institution = location.get("Institution", "Unknown")

                # Create or update Location node
                location_node = session.run("""
                    MERGE (l:Location {Institution: $Institution, City: $City, Country: $Country})
                    ON CREATE SET l.Institution = $Institution, l.City = $City, l.Country = $Country
                    ON MATCH SET l += {Institution: $Institution, City: $City, Country: $Country}
                    RETURN l
                """, Institution=institution, City=city, Country=country).single()["l"]
                session.run("""
                    MATCH (t:Trial {TrialID: $TrialID}), (l:Location {Institution: $Institution, City: $City, Country: $Country})
                    MERGE (t)-[:CONDUCTED_AT]->(l)
                """, TrialID=data["Trial"]["Trial ID"], Institution=institution, City=city, Country=country)
            else:
                print(f"Skipped a location due to insufficient data: {location}")

# Function to clean unwanted unicode characters like "\u00e9" from a string
def clean_unicode(text):
    if isinstance(text, str):
        return text.encode('ascii', 'ignore').decode('ascii')
    return text

# Updated function to include different intervention types and convert each row to a JSON-like structure
def row_to_json(row):
    trial_info = {
        "Trial ID": clean_unicode(row["NCT Number"]),
        "Title": clean_unicode(row["Study Title"]),
        "URL": clean_unicode(row["Study URL"]),
        "Status": clean_unicode(row["Study Status"]),
        "Brief Summary": clean_unicode(row["Brief Summary"]),
        "Phase": clean_unicode(row["Phases"]),
        "Study Start Date": clean_unicode(row["Start Date"]),
        "Expected Completion Date": clean_unicode(row["Completion Date"])
    }

    # Splitting interventions into different types if they exist
    intervention_types = ["drug", "procedure", "device", "behavioral", "combination_product","biological","radiation","other"]
    interventions_info = {key.capitalize(): [] for key in intervention_types}  # Initialize all intervention types with empty lists
    if pd.notnull(row["Interventions"]):
        interventions = row["Interventions"].split('|')
        for intervention in interventions:
            intervention = intervention.strip()
            for type_key in intervention_types:
                if intervention.startswith(f"{type_key}:"):
                    # Clean the intervention name and add it to the corresponding list
                    intervention_name = intervention[len(f"{type_key}:"):].strip()
                    intervention_cleaned = clean_unicode(intervention_name)
                    # Capitalize the first letter of each intervention type for the output
                    intervention_type_key = type_key.capitalize()
                    interventions_info[intervention_type_key].append(intervention_cleaned)

    # Splitting disease names if multiple diseases are listed
    disease_info = {
        "Disease Name": [clean_unicode(disease) for disease in row["Conditions"].split('|')] if pd.notnull(row["Conditions"]) else []
    }

    # Parsing locations into structured format
    locations_info = []
    if pd.notnull(row["Locations"]):
        locations_list = row["Locations"].split('|')
        for location in locations_list:
            parts = [clean_unicode(part.strip()) for part in location.split(',')]
            location_dict = {
                "Institution": parts[0] if parts else None,
                "City": parts[1] if len(parts) > 1 else None,
                "Country": parts[-1] if parts else None
            }
            locations_info.append(location_dict)

    # Structuring the JSON object
    json_structure = {
        "Trial": trial_info,
        "Drug/Intervention": interventions_info,
        "Disease/Condition": disease_info,
        "Locations": locations_info
    }

    return json_structure





df_clinical = pd.read_csv(file_path)
preprocessed_trials = preprocess(df_clinical)

# Convert each row of the dataframe to JSON structure and store in a list
json_data = [row_to_json(row) for index, row in preprocessed_trials.iterrows()]

# Convert the list to JSON string for display
json_string = json.dumps(json_data, indent=4)

# Display the first few JSON structures as a sample
print(json_string[:10000])  # Display only first 2000 characters for brevity