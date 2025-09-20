import os
import matplotlib.pyplot as plt
import numpy as np

# Set up paths
base_dir = os.getcwd()
data_path = os.path.join(base_dir, '')
data_path_takin = os.path.join(base_dir, 'takin_analysis_soft_mode_1p45meV')
save_path = os.path.join(base_dir, 'plots/')

# Create the plots directory if it doesn't exist
os.makedirs(save_path, exist_ok=True)

# Exp Info
Project="sample_ExpID"

##### format: 'filename':('delta_q', 'temperature')
##### Set the filename to None if you don't want to plot this data
# Rawdata files
file_labels = {
    '2-20_300mK_CuCu_delta_0p000': ('0.0',    '0.3'),
    '2-20_300mK_CuCu_delta_0p015': ('-0.015', '0.3'),
    '2-20_300mK_CuCu_delta_0p030': ('-0.03',  '0.3'),
}

# Takin simulation data files
file_labels_takin = {
    '2-20_300mK_CuCu_delta_0p000.dat': ('0.0',    '0.3'),
    '2-20_300mK_CuCu_delta_0p015.dat': ('-0.015', '0.3'),
    '2-20_300mK_CuCu_delta_0p030.dat': ('-0.03',  '0.3')}


# Common column names for processing
cols_raw = ['QH', 'QK', 'QL', 'EN', 'M1', 'CNTS']
cols_takin = ['h', 'k', 'l', 'E', 'S(Q,E)']

# Plotting parameters
plot_params = {
    'font_family': 'Times New Roman',
    'font_size': 18,
    'xmin': 0,
    'xmax': 16.25,
    'xx': 2,
    'ymin': 0,
    'ymax': 0.0018,
    'yy': 0.0005,
    'title_2d': r'SrTiO$_3$, (2 -2 0) + $\Delta$ * (-1 -1 0), $T$ = 0.300 K, IN8-Cu/Cu',
    'title_3d': r'SrTiO$_3$, G=(2 2 0) + $\Delta$ * (1 -1 0), $T$ = 0.300 K, Cu/Cu',
    'output_2d_filename': 'test.png',
    'output_3d_filename': 'test_3d.png'
}

# Takin specific parameters
takin_params = {
    'scale': 3e6,
    'offset': 0.00015
}

# Matplotlib configuration 
plt.rc('font', **{'family': plot_params['font_family'], 
                  'size': plot_params['font_size']})
