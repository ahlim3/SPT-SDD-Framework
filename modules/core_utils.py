import os
import json
import numpy as np
import pandas as pd
from collections import defaultdict

class CommonApp:
    def __init__(self):
        self.dose_cache = {}
        self.sdd_cache = {}
        self.energy_map = {}

    @staticmethod
    def load_config(path):
        with open(path, "r") as f:
            return json.load(f)

    def get_energy_grid(self, folder):
        files = [f for f in os.listdir(folder) if f.endswith("MeV.csv")]
        grid = []
        for f in files:
            e_str = f.replace("MeV.csv", "")
            e_val = float(e_str)
            grid.append(e_val)
            self.energy_map[e_val] = e_str
        return np.sort(np.array(grid))

    @staticmethod
    def get_spectrum_cdf(phsp_path, bin_edges):
        with open(phsp_path, "r") as f:
            energies = [float(l.split()[5]) for i, l in enumerate(f) if i >= 9]
        hist, _ = np.histogram(energies, bins=bin_edges)
        pdf = hist / np.sum(hist)
        return np.cumsum(pdf), pdf

    @staticmethod
    def get_high_let_lambda(mean_dose_csv, pdf, assigned_dose):
        if mean_dose_csv == "None" or not os.path.exists(mean_dose_csv):
            return None
        z1_values = pd.read_csv(mean_dose_csv)["Average Dose"].to_numpy(dtype=float)
        mean_z1 = np.sum(z1_values[:len(pdf)] * pdf)
        return assigned_dose / mean_z1

    def get_dose_array(self, energy, folder):
        key_str = self.energy_map[energy]
        if key_str not in self.dose_cache:
            path = os.path.join(folder, f"{key_str}MeV.csv")
            df = pd.read_csv(path)
            self.dose_cache[key_str] = df["Dose"].to_numpy(dtype=float)
        return self.dose_cache[key_str]

    def get_sdd_groups(self, energy, folder):
        key_str = self.energy_map[energy]
        if key_str not in self.sdd_cache:
            path = os.path.join(folder, f"{key_str}MeV.txt")
            groups = defaultdict(list)
            with open(path, "r") as f:
                for line in f:
                    try:
                        pid = int(line.split(";")[0].split(",")[1])
                        groups[pid].append(line)
                    except: continue
            self.sdd_cache[key_str] = groups
        return self.sdd_cache[key_str]