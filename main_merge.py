"""
Python3 Script to merge multiple scans for INS data collected at ILL

Last updated: Sept 2025
License: GNU-V2
Author: [Shiyu Deng]
Email:[dengs@ill.fr] or [sd864@cantab.ac.uk]
"""

from functions import *
import sys
import os

def main():
    # Check for command-line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.py>")
        return
    input_file_path = sys.argv[1]

    try:
        input = load_config_from_file(input_file_path)
    except FileNotFoundError:
        print(f"Error: The input file '{input_file_path}' was not found.")
        return
    
    os.makedirs(input.save_dir, exist_ok=True)

    print("--- Merge Multiple Scan Raw Data files ---")
    merge_data(input.file_list, input.file_dir, 
               input.save_file, input.save_dir,
               input.ScanConstant, input.step_size)

if __name__ == "__main__":
    main()