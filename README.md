# TAS-INS Phonon Measurement Python Scripts

Useful python scripts to deal with the STO experimental data :)

Rawdata format:
IN8, ILL

### Workflow

1. Merge Multiple Scan RawData file
  example usage:  ``` $ python3 main_mergy.py input_merge.py ```
  Input example (input_merge.py): 
    ```
    file_list = ["042802","042807"]
    file_dir = "./rawdata"

    save_file = "2-20_300mK_CuCu_E_9meV"
    save_dir="./merged_data"

    # Merge rule; step size; the tolerance for grouping the data
    ScanConstant = "EN"  # constant "QH" or "EN"
    step_size = 0.005  # step size in QH in constant-E scan; step size in EN in constant-Q scan
    ```

2. Analyze the Data:
- Use Takin2.0 to analyze the data: 
phonon dispersion (E(q)) convoluted with TAS resolutions 

3. Summary Plot:
Load data from
- original data from main_merge.py
- fitted data from Takin2.0 output
Plot the datasets (if exists) in 2D or 3D. 
``` $ python3 INSpy_main.py -in input_analysis.py -plot 3D ```

---
Last updated:
2025-09-15
Shiyu DENG (dengs@ill.fr)
