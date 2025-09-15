merge_rules_QH = {
    'key_columns': ['QH'],
    'value_columns': {
        'PNT': 'first',
        'QH': 'first', # keep the first non-null value
        'QK': 'first',
        'QL': 'first', 
        'EN': 'first',
        'M1': 'sum',
        'M2': 'sum',        
        'TIME': 'sum',       
        'CNTS': 'sum',
        'A2': 'first',
        'A3': 'first',
        'A4': 'first',
        'A6': 'first',
        'QM': 'first',
        'TT': 'first',
        'TRT': 'first',
        'GU': 'first',
        'GL': 'first',
        'tolerance_bins': 'first'
    }
}


merge_rules_EN = {
    'key_columns': ['EN'],
    'value_columns': {
        'PNT': 'first',
        'QH': 'first', # keep the first non-null value
        'QK': 'first',
        'QL': 'first', 
        'EN': 'first',
        'M1': 'sum',
        'M2': 'sum',        
        'TIME': 'sum',       
        'CNTS': 'sum',
        'A2': 'first',
        'A3': 'first',
        'A4': 'first',
        'A6': 'first',
        'QM': 'first',
        'TT': 'first',
        'TRT': 'first',
        'GU': 'first',
        'GL': 'first',
        'tolerance_bins': 'first'
    }
}
