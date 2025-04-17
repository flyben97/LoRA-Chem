import pandas as pd
import os
from datetime import datetime

# Define the input and output folder paths
input_folder = 'files'
output_folder = 'output'
report_file = f'processing_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List of common encodings to try
ENCODINGS = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']

# Function to generate natural language description for a reaction
def generate_reaction_description(row):
    template = (
        "The reaction uses {Ligand_Compound_Name} as ligand with SMILES {Ligand_SMILES}, "
        "producing {Product_Compound_Name} with SMILES {Product_SMILES}. "
        "The reaction temperature is {Temp} K, "
        "using ligand type {L_Type} "
        "in a {R_Type} type reaction."
    )
    description = template.format(
        Ligand_Compound_Name=row['Ligand_Compound_Name'],
        Product_Compound_Name=row['Product_Compound_Name'],
        Ligand_SMILES=row['Ligand_SMILES'],
        Product_SMILES=row['Product_SMILES'],
        Temp=row['Temp (K)'],
        L_Type=row['L_Type'],
        R_Type=row['R_Type']
    )
    return description

# Initialize report content
report_lines = [f"Processing Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
report_lines.append("=" * 50 + "\n")

# Get all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
total_rows_removed = 0
successful_files = 0

# Function to read CSV with encoding fallback
def read_csv_with_encoding(file_path):
    for encoding in ENCODINGS:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df, encoding, None
        except UnicodeDecodeError as e:
            continue
        except Exception as e:
            return None, encoding, str(e)
    return None, None, "Failed to decode with any supported encoding"

# Process each CSV file
for csv_file in csv_files:
    input_file = os.path.join(input_folder, csv_file)
    output_file = os.path.join(output_folder, 
                             f"{os.path.splitext(csv_file)[0]}_reaction_descriptions_merged.csv")
    
    try:
        # Try reading the file with different encodings
        df, used_encoding, error = read_csv_with_encoding(input_file)
        
        if df is None:
            raise Exception(f"Encoding error: {error}")
            
        initial_rows = len(df)
        
        # Remove empty rows
        df = df.dropna(how='all')
        rows_after_cleaning = len(df)
        rows_removed = initial_rows - rows_after_cleaning
        
        if rows_after_cleaning == 0:
            report_lines.append(f"{csv_file}:\n")
            report_lines.append(f"  Status: Failed - No valid data after removing empty rows\n")
            report_lines.append(f"  Initial rows: {initial_rows}\n")
            report_lines.append(f"  Rows removed: {rows_removed}\n")
            report_lines.append(f"  Encoding attempted: {used_encoding}\n\n")
            print(f"Skipping {csv_file} - No valid data after cleaning")
            continue
        
        # Generate descriptions
        df['Description'] = df.apply(generate_reaction_description, axis=1)
        
        # Save the processed file
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        # Update report
        report_lines.append(f"{csv_file}:\n")
        report_lines.append(f"  Status: Successfully processed\n")
        report_lines.append(f"  Initial rows: {initial_rows}\n")
        report_lines.append(f"  Rows removed: {rows_removed}\n")
        report_lines.append(f"  Encoding used: {used_encoding}\n")
        report_lines.append(f"  Output file: {output_file}\n\n")
        
        total_rows_removed += rows_removed
        successful_files += 1
        print(f"Processed {csv_file}: {rows_removed} empty rows removed, encoding: {used_encoding}, saved to {output_file}")
        
    except Exception as e:
        report_lines.append(f"{csv_file}:\n")
        report_lines.append(f"  Status: Failed\n")
        report_lines.append(f"  Error: {str(e)}\n\n")
        print(f"Error processing {csv_file}: {str(e)}")

# Add summary to report
report_lines.append("=" * 50 + "\n")
report_lines.append("Summary:\n")
report_lines.append(f"Total files processed: {len(csv_files)}\n")
report_lines.append(f"Successfully processed files: {successful_files}\n")
report_lines.append(f"Failed files: {len(csv_files) - successful_files}\n")
report_lines.append(f"Total empty rows removed: {total_rows_removed}\n")

# Write report to file
with open(os.path.join(output_folder, report_file), 'w') as f:
    f.writelines(report_lines)

# Print final completion message
print(f"\nBatch processing completed.")
print(f"Processed {len(csv_files)} files, removed {total_rows_removed} empty rows")
print(f"Report saved to: {os.path.join(output_folder, report_file)}")