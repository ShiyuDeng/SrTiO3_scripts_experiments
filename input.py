file_list = ['042802','042807']
file_dir = "./rawdata"

save_file = "2-20_300mK_CuCu_E_9meV"
save_dir="./merged_data"

# Merge rule; step size; the tolerance for grouping the data
ScanConstant = "EN"  # constant "QH" or "EN"
step_size = 0.005  # step size in QH in constant-E scan; step size in EN in constant-Q scan
