"""
functions to read/merge/plot INS data
Last updated: Sept 2025
License: GNU-V2
Author: [Shiyu Deng]
Email:[dengs@ill.fr] or [sd864@cantab.ac.uk]
"""
#####################################################
################## functions ########################
### 1. read input.py file                         ###
### 2. merge the INS scan data by constant Q or E ###
### 3. read the INS data and plot                 ###
#####################################################

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import importlib.util

from MergeRule import merge_rules_QH, merge_rules_EN

###########  read input.py file  #################
def load_config_from_file(filepath):
    """
    Dynamically loads configuration from a specified Python file.
    Here. the 'inpput.py' for different analysis tasks
    """
    spec = importlib.util.spec_from_file_location("input_module", filepath)
    input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(input_module)
    return input_module
########### END -  read input.py file  #################


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



############  READ INS Rawdata files ######
def read_data(data_path, file_labels, cols_raw):
    """Reads and processes original scan files."""
    data_all = pd.DataFrame()
    print("Reading original data...")
    for filename, (delta, temp) in file_labels.items():
        file_path = os.path.join(data_path, filename)
        data = pd.read_csv(file_path, delim_whitespace=True, skiprows=58, header=0, usecols=cols_raw)
        data["$\\Delta$"] = float(delta)
        data["CNTS_normalized"] = data["CNTS"] / data["M1"]
        data["CNTS_err"] = np.sqrt(data["CNTS"]) / data["M1"]
        data_all = pd.concat([data_all, data], ignore_index=True)
    return data_all


##############  READ Takin Output Simulation Results #####################
def read_data_takin(data_path, file_labels, cols_takin, scale, offset):
    """Reads and processes takin simulation data."""
    data_all_takin = pd.DataFrame()
    print("Reading takin simulation data...")
    for filename, (delta, temp) in file_labels.items():
        file_path = os.path.join(data_path, filename)
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, comment='#', names=cols_takin)
        data["CNTS_normalized"] = data["S(Q,E)"] * scale + offset
        data["$\\Delta$"] = float(delta)
        data_all_takin = pd.concat([data_all_takin, data], ignore_index=True)
    return data_all_takin


################## overplot in 2D ##################
def plot_2d_data(data_all, data_all_takin, params, output_filepath):
    """Generates and saves a 2D plot."""
    plt.figure(figsize=(10, 6))
    # Plot original data if available
    if not data_all.empty:
        plt.errorbar(x=data_all['EN'], y=data_all['CNTS_normalized'], yerr=data_all['CNTS_err'],
                    fmt='none', capsize=1.5, lw=0.5, alpha=0.7)
        sns.scatterplot(data=data_all, x="EN", y="CNTS_normalized",
                        style="$\\Delta$", markers=True,
                        hue="$\\Delta$", palette="viridis",
                        s=80, alpha=0.8)
        
    # Plot takin data if available
    if not data_all_takin.empty:
        sns.lineplot(data=data_all_takin, x='E', y='CNTS_normalized',
                    hue='$\\Delta$', palette="viridis",
                    legend=False, alpha=0.6)
        
    # plot settings
    plt.title(params['title_2d'], pad=15)
    plt.xlabel(r'Energy (meV)')
    plt.ylabel(r'Scattered Intensity (normalized)')
    plt.xlim(params['xmin'], params['xmax'])
    plt.ylim(params['ymin'], params['ymax'])
    plt.xticks(np.arange(params['xmin'], params['xmax'], step=params['xx']))
    plt.yticks(np.arange(params['ymin'], params['ymax'], step=params['yy']))
    plt.grid(alpha=0.5, linestyle='-.', lw=1.5)
    
    plt.savefig(output_filepath, dpi=900, transparent=True)
    plt.show()
    print(f"2D plot saved to {output_filepath}")


##################  overplot in 3D #################
def plot_3d_data(data_all, data_all_takin, params, output_filepath):
    """Generates and saves a 3D plot."""
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Plot original data if available
    if not data_all.empty:
        ax.errorbar(x=data_all['EN'], y=data_all['$\\Delta$'], z=data_all['CNTS_normalized'],
                    zerr=data_all['CNTS_err'], fmt='none', capsize=1.5, lw=0.2, color='lightblue', alpha=0.7)
        g = ax.scatter(data_all['EN'], data_all['$\\Delta$'], data_all['CNTS_normalized'],
                       c=data_all['$\\Delta$'], cmap="viridis", s=15)
        legend = ax.legend(*g.legend_elements(), bbox_to_anchor=(0.72, 0.85), loc=2)
        ax.add_artist(legend)

    # Plot takin data if available
    if not data_all_takin.empty:
        ax.scatter(data_all_takin['E'], data_all_takin['$\\Delta$'], data_all_takin['CNTS_normalized'],
                   c=data_all_takin['$\\Delta$'], cmap="viridis", s=0.2, alpha=0.5)

    # plot settings
    ax.set_title(params['title_3d'], pad=15)
    ax.set_xlabel(r'Energy (meV)')
    ax.set_ylabel(r'$\Delta$*[1-10] for phonon propagation')
    ax.set_zlabel(r'Scattered Intensity (normalized)')
    ax.set_xlim(params['xmin'], params['xmax'])
    ax.set_ylim(-0.070, 0.0)
    ax.set_zlim(params['ymin'], 0.0018)
    ax.set_xticks(np.arange(params['xmin'], params['xmax'], step=params['xx']))
    ax.set_yticks(np.arange(-0.070, 0.0, step=0.015))
    ax.set_zticks(np.arange(params['ymin'], params['ymax'], step=params['yy']))
    ax.set_box_aspect(aspect=(1.8, 1.2, 1.2))

    plt.savefig(output_filepath, dpi=900, transparent=True, bbox_inches='tight')
    plt.show()
    print(f"3D plot saved to {output_filepath}")