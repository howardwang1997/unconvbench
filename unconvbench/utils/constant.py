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

DATASETS_MAP = { # need removal
    'unconvbench_supercon': {'path': '../datasets/jarvis_epc_data_figshare_1058.json', 'label': 'Tc'},
    'unconvbench_exfoliation': {'path': '../datasets/2dmatpedia_exfoliation.json', 'label': 'exfoliation_energy_per_atom'},
    'unconvbench_2d_gap':  {'path': '../datasets/c2db_atoms.json', 'label': 'gap'},
    'unconvbench_2d_e_tot':  {'path': '../datasets/c2db_atoms.json', 'label': 'etot'},
    'unconvbench_co2_adsp':  {'path': '../datasets/hmof_sub.json', 'label': 'max_co2_adsp'},
    'unconvbench_qmof':  {'path': '../datasets/qmof_sub.json', 'label': 'energy_total'},
    'unconvbench_defected':  {'path': '../datasets/vacancydb.json', 'label': 'ef'},
    'unconvbench_src_bulk':  {'path': '../datasets/jdftvac.json', 'label': 'ef'},
    'unconvbench_bulk_s':  {'path': '../datasets/eform_s.json', 'label': 'eform'},
    'unconvbench_bulk_m':  {'path': '../datasets/eform_m.json', 'label': 'eform'},
    'unconvbench_bulk_l':  {'path': '../datasets/eform_l.json', 'label': 'eform'},
}
