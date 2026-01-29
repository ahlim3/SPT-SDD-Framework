import numpy as np

class DoseEngine:
    def __init__(self, rng_seed=None):
        self.rng = np.random.default_rng(rng_seed)

    def sample_energy(self, cdf, bin_edges):
        idx = np.searchsorted(cdf, self.rng.random())
        idx = min(idx, len(bin_edges) - 2)
        return bin_edges[idx + 1] if self.rng.random() > 0.5 else bin_edges[idx]

    def get_high_let_count(self, lambda_p):
        return int(self.rng.poisson(lam=lambda_p))

    def get_low_let_tracks(self, target_dose, cdf, grid, app, dose_folder, tolerance=0.01):
        dose_sum = 0.0
        accepted_tracks = []
        while dose_sum < (target_dose - tolerance):
            E = self.sample_energy(cdf, grid)
            dose_array = app.get_dose_array(E, dose_folder)
            tidx = self.rng.integers(0, len(dose_array))
            d = dose_array[tidx]

            if d > (target_dose - dose_sum) and self.rng.random() < 0.9:
                continue
            dose_sum += d
            accepted_tracks.append((E, tidx))
        return accepted_tracks, dose_sum