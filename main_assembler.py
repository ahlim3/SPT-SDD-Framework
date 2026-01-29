import os
import numpy as np
from modules.core_utils import CommonApp
from modules.dose_engine import DoseEngine
from modules.sdd_io import SDDWriter

def main(config_path):
    app = CommonApp()
    config = app.load_config(config_path)
    engine = DoseEngine(rng_seed=config["simulation"].get("rng_seed"))
    writer = SDDWriter(config["simulation"]["incident_pdg"])

    dose_folder = config["paths"]["dose_file_folder"]
    grid = app.get_energy_grid(dose_folder)
    cdf, pdf = app.get_spectrum_cdf(config["paths"]["target_spectrum"], grid)
    
    is_high_let = config["simulation"]["simulation_type"] in ["high_let"]
    lambda_p = app.get_high_let_lambda(config["paths"]["mean_dose_csv_path"], pdf, config["simulation"]["assigned_dose"]) if is_high_let else None

    dose_rate = config["simulation"].get("dose_rate_Gy_per_min", 0)
    dose_rate_s = dose_rate / 60.0 if dose_rate > 0 else 0

    output_dir = config["paths"]["output_folder"]
    os.makedirs(output_dir, exist_ok=True)

    for i in range(config["simulation"]["total_simulations"]):
        all_track_data, sampled_energies = [], []
        
        if is_high_let:
            n_particles = engine.get_high_let_count(lambda_p)
            total_dose = 0.0
            for _ in range(n_particles):
                E = engine.sample_energy(cdf, grid)
                sampled_energies.append(E)
                d = app.get_dose_array(E, dose_folder)
                tidx = engine.rng.integers(0, len(d))
                total_dose += d[tidx]
                all_track_data.append(app.get_sdd_groups(E, config["paths"]["DSB_file_folder"]).get(tidx, []))
            primary_count = n_particles
            track_times = None
        else:
            tracks, total_dose = engine.get_low_let_tracks(config["simulation"]["assigned_dose"], cdf, grid, app, dose_folder)
            primary_count = len(tracks)
            
            track_times = None
            if dose_rate_s > 0:
                total_time_s = config["simulation"]["assigned_dose"] / dose_rate_s
                dt = total_time_s / primary_count
                track_times = [int(round((k + 1) * dt) * 1e9) for k in range(primary_count)]
            
            for E, tidx in tracks:
                sampled_energies.append(E)
                all_track_data.append(app.get_sdd_groups(E, config["paths"]["DSB_file_folder"]).get(tidx, []))

        mean_E = np.mean(sampled_energies) if sampled_energies else 0.0
        writer.save(os.path.join(output_dir, f"cell_{i}.sdd"), 
                    total_dose, 0, primary_count, mean_E, all_track_data, dose_rate_s, track_times)
        print(f"Cell {i} complete: Dose={total_dose:.4f} Gy, Tracks={primary_count}")

if __name__ == "__main__":
    #config_path = "proton_config.json"
    config_path = "alpha_config.json"
    # config_path = "electron_config_time.json"
    main(config_path)    