VERSION = '1.0.1'

DATASETS_LEN = {
    'unconvbench_supercon': 1058,
    'unconvbench_exfoliation': 4527,
    'unconvbench_2d_gap': 3520,
    'unconvbench_2d_e_tot': 3520,
    'unconvbench_co2_adsp': 13765,
    'unconvbench_qmof': 5106,
    'unconvbench_defected': 530,
    'unconvbench_src_bulk': 530,
    'unconvbench_bulk_s': 5000,
    'unconvbench_bulk_m': 5000,
    'unconvbench_bulk_l': 5000,
}

DATASETS_RESULTS = {}
for k in DATASETS_LEN.keys():
    DATASETS_RESULTS[k] = {'fold_0': [], 'fold_1': [], 'fold_2': [], 'fold_3': [], 'fold_4': []}

PRESET_MAPPER = {
    '2d_materials': ['unconvbench_exfoliation', 'unconvbench_2d_gap', 'unconvbench_2d_e_tot'],
    'MOF': ['unconvbench_co2_adsp', 'unconvbench_qmof'],
    'defected': ['unconvbench_supercon', 'unconvbench_defected'],
    'sizes': ['unconvbench_bulk_s', 'unconvbench_bulk_m', 'unconvbench_bulk_l'],
    'defected_bulk': ['unconvbench_defected', 'unconvbench_src_bulk']
}
