from functions import *

import pandas as pd
import sys
import os
import importlib.util

def load_config_from_file(filepath):
    """
    Dynamically loads configuration from a specified Python file.
    """
    spec = importlib.util.spec_from_file_location("input_module", filepath)
    input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(input_module)
    return input_module

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