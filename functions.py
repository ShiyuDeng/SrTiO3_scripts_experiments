### functions ###
### merge the INS scan data by constant Q or E ###

import pandas as pd
import os
import numpy as np
from MergeRule import merge_rules_QH, merge_rules_EN

###### group constant QH or EN scans #####
def merge_data(file_list, file_dir, save_file, save_dir,
               ScanConstant, step_size):

    # Use a dictionary to select the correct rules and grouping column
    rule_map = {
        "QH": {"rules": merge_rules_QH, "col": "EN"},
        "EN": {"rules": merge_rules_EN, "col": "QH"}
    }
    
    # Get the rules and column for the specified ScanConstant
    if ScanConstant not in rule_map:
        print(f"Error: Invalid 'ScanConstant' value '{ScanConstant}'. Must be 'QH' or 'EN'.")
        return
        
    merge_rules = rule_map[ScanConstant]["rules"]
    group_by_col = rule_map[ScanConstant]["col"]

    #### read the data files ####
    merged_df = pd.DataFrame()

    # Loop through the files in the directory
    for file in file_list:
        # Read the file into a data frame
        file_path = os.path.join(file_dir, file)
        print(f'Reading file: {file_path}')
        try:
            df = pd.read_csv(file_path, skiprows=58, delim_whitespace=True, dtype=np.float64)
            # df['file_name'] = file
            print(f'Processing file {file}')
            print(df.to_string()) 

            merged_df = pd.concat([merged_df, df], ignore_index=True)
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping.")
        
    if merged_df.empty:
        print("No data was loaded. Exiting.")
        return

    # Check for missing values
    print(f'Finished processing file {file}')
    print(f'Number of rows: {len(merged_df)}')
    print(f'Number of missing values in CNTS column: {merged_df["CNTS"].isna().sum()}')

    ###### merge the data by constant QH or EN ######
    # tolerance bins: Get the tolerance bins by rounding the QH/EN values to the nearest multiple of the step size
    merged_df['tolerance_bins'] = np.round(merged_df[group_by_col] / step_size) * step_size
    print(f'Merge by constant {ScanConstant}, with the tolerance bins: {merged_df["tolerance_bins"].unique()}')

    processed_df = merged_df.groupby('tolerance_bins').agg(merge_rules['value_columns']).reset_index(drop=True)
    processed_df = processed_df.loc[:, ~processed_df.columns.duplicated()]
    print(f'The Merge data')
    print(processed_df.to_string()) 

    ####### write the save file ####
    # Read the first 58 rows from one of the input files as text
    header_rows = ""
    try:
        with open(os.path.join(file_dir, file_list[0]), 'r') as f:
            header_rows = ''.join(f.readlines()[:58])
        savepath = os.path.join(save_dir, save_file + '.txt')
    except (FileNotFoundError, IndexError):
        print("Warning: Could not read header from original file.")

    # Save the merged data frame to a text file with aligned columns
    with open(savepath, 'w') as f:
        f.write(header_rows)
        # Use to_string() with the desired separator and alignment options
        f.write(processed_df.to_string(index=False, header=True, justify='left', col_space=10))
    
    print(f"\nSuccessfully processed and saved data to {savepath}")