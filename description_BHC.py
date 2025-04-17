import pandas as pd
import os

# Define the input and output folder paths
input_folder = 'files'  # Input folder containing CSV files
output_folder = 'output'  # Output folder name

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to generate natural language description for a reaction
def generate_reaction_description(row):
    # Updated template with new column names
    template = (
        "The first reactant is {Aryl_halide_Compound_Name} with SMILES {Aryl_halide_smiles}, "
        "using {Ligand_Compound_Name} as ligand with SMILES {Ligand_smiles}, "
        "{Base_Compound_Name} as base with SMILES {Base_smiles}, "
        "and {Additive_Compound_Name} as additive with SMILES {Additive_smiles}. "
        "This is a Buchwald-Hartwig Cross-Coupling reaction."
    )
    # Fill the template with data from the row using new column names
    description = template.format(
        Aryl_halide_Compound_Name=row['Aryl halide_Compound_Name'],
        Ligand_Compound_Name=row['Ligand_Compound_Name'],
        Base_Compound_Name=row['Base_Compound_Name'],
        Additive_Compound_Name=row['Additive_Compound_Name'],
        Aryl_halide_smiles=row['Aryl halide_smiles'],
        Ligand_smiles=row['Ligand_smiles'],
        Base_smiles=row['Base_smiles'],
        Additive_smiles=row['Additive_smiles']
    )
    return description

# Get all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Process each CSV file
for csv_file in csv_files:
    # Construct full input and output file paths
    input_file = os.path.join(input_folder, csv_file)
    output_file = os.path.join(output_folder, 
                             f"{os.path.splitext(csv_file)[0]}_reaction_descriptions_merged.csv")
    
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(input_file)
        
        # Apply the function to each row to generate descriptions
        df['Description'] = df.apply(generate_reaction_description, axis=1)
        
        # Save the entire DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        
        # Print confirmation message for each file
        print(f"Natural language descriptions have been generated and merged into {output_file}")
    
    except Exception as e:
        print(f"Error processing {csv_file}: {str(e)}")

# Print final completion message
print(f"\nBatch processing completed. Processed {len(csv_files)} files.")


