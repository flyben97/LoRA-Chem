import pandas as pd
import json
import os

# Function to create instruction string from description
def create_instruction(description, yield_value):
    return {
        "instruction": "What is the yield of this reaction?",
        "input": f"{description}",
        "output": f"OK, this is a SHC-oAK reaction. Based on the chemical reaction information you provided, the yield of this reaction is: {str(yield_value)}%.",
        "history": []
    }

# Define input and output directories
input_folder = 'output'
output_dir = 'output/json_conversions'  # New subfolder for JSON outputs

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all processed CSV files from the previous script
csv_files = [f for f in os.listdir(input_folder) if f.endswith('_reaction_descriptions_merged.csv')]

# Process each CSV file
for csv_file in csv_files:
    try:
        # Construct input file path
        input_file = os.path.join(input_folder, csv_file)
        
        # Generate output filename based on input filename
        base_name = os.path.splitext(csv_file)[0].replace('_reaction_descriptions_merged', '')
        json_filename = f'{base_name}.json'
        
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Extract required columns
        data = df[['Description', 'Yield']]
        
        # Convert data to JSON format
        json_data = [create_instruction(row['Description'], row['Yield']) for _, row in data.iterrows()]
        with open(os.path.join(output_dir, json_filename), 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully processed {csv_file} into {json_filename}")
        
    except Exception as e:
        print(f"Error processing {csv_file}: {str(e)}")

print(f"\nBatch processing completed. Processed {len(csv_files)} files.")