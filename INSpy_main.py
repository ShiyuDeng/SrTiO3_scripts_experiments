"""
Python3 Script to analyze/plot INS data

Last updated: Sept 2025
License: GNU-V2
Author: [Shiyu Deng]
Email:[dengs@ill.fr] or [sd864@cantab.ac.uk]
"""

# main.py
from functions import *
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Analyze and plot INS data from a configuration file.")
    parser.add_argument("-in", "--input", dest="input_file", required=True,
                        help="Path to the input configuration file (e.g., input_analysis.py)")
    parser.add_argument("-plot", "--plot_type", choices=['2D', '3D'], default='2D',
                        help="Choose plot type: '2D' or '3D'. Default is '2D'.")

    args = parser.parse_args()

    # Load configuration dynamically from the specified input file
    try:
        config = load_config_from_file(args.input_file)
    except FileNotFoundError as e:
        print(e)
        return
    except AttributeError as e:
        print(e)
        return
    
    # Check if a plot type is selected, otherwise provide a warning
    if args.plot_type not in ['2D', '3D']:
        print("Choose a valid plot type: '2D' or '3D'.")
        return
    
    # Load Data if the file_labels are provided
    data_all = pd.DataFrame()
    if config.file_labels:
        data_all = read_data(config.data_path, config.file_labels, config.cols_raw)

    data_all_takin = pd.DataFrame()
    if config.file_labels_takin:
        data_all_takin = read_data_takin(config.data_path_takin, config.file_labels_takin,
                                        config.cols_takin, config.takin_params['scale'], config.takin_params['offset'])
    ### debug test
    print("Data from Raw files:")
    print(data_all.to_string())
    # print("Data from Takin simulation files:")
    # print(data_all_takin.to_string())

    # Plot the data
    if args.plot_type == '2D':
        if data_all.empty and data_all_takin.empty:
            print("No data was loaded for the 2D plot. Exiting.")
        else:
            output_filepath = os.path.join(config.save_path, config.plot_params['output_2d_filename'])
            plot_2d_data(data_all, data_all_takin, config.plot_params, output_filepath)
    elif args.plot_type == '3D':
        if data_all.empty and data_all_takin.empty:
            print("No data was loaded for the 3D plot. Exiting.")
        else:
            output_filepath = os.path.join(config.save_path, config.plot_params['output_3d_filename'])
            plot_3d_data(data_all, data_all_takin, config.plot_params, output_filepath)

if __name__ == "__main__":
    main()