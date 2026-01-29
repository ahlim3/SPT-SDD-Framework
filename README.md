# SPT–SDD Sampling Framework

This repository provides a **shareable core code and tool framework** for spectrum-driven particle track (SPT) sampling and SDD file generation, developed to support reproducible radiobiological simulations.

Large pre-calculated SDD libraries, phase-space files, and HPC-specific scripts are intentionally excluded due to size and infrastructure constraints. Instead, this framework enables users to **reproduce the sampling, superposition, and dose-matching logic** using their own data.

---

## 1. Scope of This Repository

### Included (public)
- SPT–SDD sampling core code (high-LET / low-LET)
- Superposition and dose-matching logic
- Optional dose-rate–based timestamp handling
- Modular Python framework
- Example configuration files
- End-to-end assembly pipeline

### Excluded (not public)
- Full pre-calculated SDD libraries  
- Full TOPAS input decks  
- Phase-space files  
- HPC job submission scripts  

These excluded components are large (>10–100 GB) and experiment-specific but **are not required to understand or reproduce the methodology**.

---

## 2. Directory Structure

```
project_root/
├─ modules/
│  ├─ core_utils.py        # Energy grid, PDF/CDF, config utilities
│  ├─ dose_engine.py       # High-/low-LET dose & particle sampling logic
│  └─ sdd_io.py            # SDD writer, PID reindexing, timestamp handling
│
├─ main_assembler.py       # Main pipeline entry point
│
├─ alpha_config.json       # Example high-LET configuration
├─ electron_config_time.json  # Example low-LET (with dose-rate) config
└─ proton_config.json     # Example proton configuration
```

---

## 3. Methodological Overview

The framework implements a **three-step workflow**:

1. **Spectrum-driven sampling**  
   Particle energies are sampled from a user-provided spectrum (PHSP-derived).  
   Energy binning and PDF/CDF construction are handled automatically.

2. **Dose and particle count determination**  
   - High-LET: particle counts are sampled using a Poisson process based on mean dose per particle.  
   - Low-LET: particles are accumulated until the assigned dose is reached (dose matching).

3. **SDD assembly and post-processing**  
   - Track-level SDD fragments are merged into a single SDD file.  
   - Particle IDs (PID) are reindexed starting from 0.  
   - The first entry of each new PID is enforced with `type = 1`.  
   - Optional timestamps are appended when dose-rate information is provided.

---

## 4. Configuration Files

All simulations are controlled via JSON configuration files.

Typical parameters include:
- Paths to dose CSV files and SDD track fragments
- Target energy spectrum (PHSP)
- Assigned dose (Gy)
- Particle type (PDG code)
- Number of simulation iterations
- Optional dose rate and RNG seed

Example configuration files:
```bash
alpha_config.json
electron_config_time.json
proton_config.json
```

Paths can be adjusted to local data without modifying the core code.

---

## 5. Running the Pipeline

From the project root:

```bash
python main_assembler.py
```

The pipeline:
- Reads the selected configuration
- Executes the appropriate sampling mode
- Writes SDD output files to the specified output directory
- Saves summary CSV statistics (dose, DSB count, particle count)

---

## 6. Reproducibility Notes

- A random seed can be specified in the configuration to ensure reproducibility.
- All numerical operations are deterministic given identical inputs.
- Energy file naming is standardized internally (e.g., `0.130MeV.csv`) to avoid floating-point inconsistencies.

---

## 7. Intended Use

This code is intended for:
- Methodological transparency
- Reproducible radiobiological modeling
- Extension to custom SDD libraries or irradiation scenarios

It is **not** intended to distribute large-scale simulation datasets.

---

## 8. Citation

If you use this framework in academic work, please cite the associated publication and acknowledge the use of this SPT–SDD sampling framework.
