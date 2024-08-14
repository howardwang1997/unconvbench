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
