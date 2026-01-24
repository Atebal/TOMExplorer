import pandas as pd
import json

def generate_unified_dax_prompt(schema_csv, rel_csv, dax_type, name, logic, target_table="N/A"):
    # 1. Extract Schema
    df_schema = pd.read_csv(schema_csv)
    df_rel = pd.read_csv(rel_csv)
    
    tables = []
    for t_name, group in df_schema.groupby('TableName'):
        tables.append({
            "table_name": t_name,
            "columns": group['ColumnName'].tolist()
        })

    # 2. Extract Relationships
    relationships = [f"{r['FromTable']}[{r['FromColumn']}] -> {r['ToTable']}[{r['ToColumn']}]" 
                     for _, r in df_rel.iterrows()]

    # 3. Combine into Unified JSON
    unified_prompt = {
        "role": "Power BI DAX Expert",
        "dax_object_type": dax_type,
        "model_context": {
            "tables": tables,
            "relationships": relationships
        },
        "request": {
            "name": name,
            "target_table": target_table,
            "logic": logic,
            "formatting": "Include comments and use VAR for complex logic"
        }
    }
    
    return json.dumps(unified_prompt, indent=2)

# --- EXAMPLES OF USAGE ---

# 1. Calculated Table Example
calc_table_logic = "Create a table of unique Products that had sales exceeding $10,000 in 2023."
# print(generate_unified_dax_prompt('schema.csv', 'rel.csv', 'Calculated Table', 'TopProducts', calc_table_logic))

# 2. Calculation Group Example
calc_group_logic = "Items: 'YTD' (TOTALYTD), 'PY' (SAMEPERIODLASTYEAR), and 'YoY %' (Difference/PY)."
# print(generate_unified_dax_prompt('schema.csv', 'rel.csv', 'Calculation Group', 'TimeIntelligence', calc_group_logic))
