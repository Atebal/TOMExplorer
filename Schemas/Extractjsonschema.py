import pandas as pd
import json

def generate_dax_prompt_json(schema_csv, relations_csv, measure_request, output_file):
    # 1. Load the CSV data
    schema_df = pd.read_csv(schema_csv)
    rel_df = pd.read_csv(relations_csv)

    # 2. Process Tables and Columns
    tables_list = []
    # Group by TableName to get a list of columns for each
    grouped = schema_df.groupby('TableName')['ColumnName'].apply(list).reset_index()
    
    for _, row in grouped.iterrows():
        tables_list.append({
            "table_name": row['TableName'],
            "columns": row['ColumnName'],
            "is_date_table": "Date" in row['TableName'] or "Calendar" in row['TableName']
        })

    # 3. Process Relationships into strings
    relationships_list = []
    for _, row in rel_df.iterrows():
        rel_string = f"{row['FromTable']}[{row['FromColumn']}] *:[1] {row['ToTable']}[{row['ToColumn']}]"
        relationships_list.append(rel_string)

    # 4. Construct the Final JSON Structure
    prompt_data = {
        "role": "Power BI DAX Expert",
        "task": "Generate a DAX measure based on the provided schema.",
        "model_context": {
            "tables": tables_list,
            "relationships": relationships_list,
            "existing_measures": {} # Can be manually filled or pulled from a 3rd CSV
        },
        "request": measure_request,
        "output_format": "DAX Code Block with inline comments"
    }

    # 5. Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(prompt_data, f, indent=2)
    
    print(f"Successfully generated {output_file}")

# --- CONFIGURATION ---
measure_req = {
    "measure_name": "New Measure Name",
    "logic_requirements": [
        "Enter your specific logic here",
        "Use Year-to-Date calculation"
    ]
}

# Run the function
# generate_dax_prompt_json('schema.csv', 'relationships.csv', measure_req, 'dax_prompt.json')
