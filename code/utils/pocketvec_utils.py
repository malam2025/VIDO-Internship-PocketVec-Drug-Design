#!/usr/bin/env python
# coding: utf-8

# # 📦 `pocketvec_utils.py` - Function Definitions

# In[ ]:


import os
import subprocess
import numpy as np
import pandas as pd
import pickle

def create_parameter_file(outfile, receptor, pocket_centroid, radius=12):
    with open(outfile, "w") as f:
        f.write(f"""RBT_PARAMETER_FILE_V1.00
TITLE example
RECEPTOR_FILE {receptor}
RECEPTOR_FLEX 0
SECTION POCKET
    CENTER {pocket_centroid}
    RADIUS {radius}
END_SECTION
""")

def environmental_variables(path_to_rDock):
    os.environ["RBT_ROOT"] = os.path.abspath(path_to_rDock)
    os.environ["RBT_HOME"] = os.path.abspath(path_to_rDock)
    os.environ["PATH"] += os.pathsep + os.path.abspath(path_to_rDock)

def create_cavity(outpath, log_file, grid_file, rbcavity="rbcavity"):
    prm = os.path.join(outpath, "st_parameters.prm")
    command = f"{rbcavity} -was -d -r {prm} > {log_file}"
    subprocess.run(command, shell=True, check=True)
    assert os.path.exists(grid_file), "Cavity grid not generated!"

def run_rDock(outpath, lib, nruns=25, seed=42):
    prm_path = os.path.join(outpath, "dock.prm")
    sd_out = os.path.join(outpath, "results.sd")
    command = f"rbdock -i {lib} -o {sd_out} -r {prm_path} -n {nruns} -s {seed}"
    subprocess.run(command, shell=True, check=True)

def create_file_scores(score_file, results_file):
    command = f"sdreport -r {results_file} -o {score_file}"
    subprocess.run(command, shell=True, check=True)

def read_rDock_scores(score_file):
    df = pd.read_csv(score_file, sep='\t')
    return dict(zip(df['Name'], df['Score']))

def raw_fp(scores, sorted_lib_file):
    with open(sorted_lib_file, 'rb') as f:
        sorted_lib = pickle.load(f)
    return np.array([scores.get(lig, 1000.0) for lig in sorted_lib])

def rank_fp(raw_scores):
    return np.argsort(np.argsort(raw_scores)).astype(np.float32)

