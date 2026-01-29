import os

class SDDWriter:
    def __init__(self, incident_pdg):
        self.incident_pdg = incident_pdg

    def save(self, path, dose, dsbs, prims, mean_E, raw_track_data, dose_rate=0, track_times=None):
        processed_body = []
        next_pid = 0
        
        for k, track_lines in enumerate(raw_track_data):
            t_int = track_times[k] if track_times else 0
            first_line_of_track = True
            for raw in track_lines:
                try:
                    s = raw.rstrip("\n")
                    if not s.endswith(";"): s += ";"
                    head, rest = s.split(";", 1)
                    
                    if next_pid == 0 and first_line_of_track: type_val = "2"
                    elif first_line_of_track: type_val = "1"
                    else: type_val = head.split(",")[0]
                    
                    # 시간 정보가 있을 경우 ns 정수 추가
                    time_suffix = f"{t_int};" if track_times else ""
                    processed_body.append(f"{type_val},{next_pid};{rest}{time_suffix}\n")
                    first_line_of_track = False
                except: continue
            next_pid += 1

        # 데이터 엔트리 마지막 필드를 1로 설정하여 시간 포함 명시
        entries = "1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0"
        if track_times: entries = entries[:-1] + "1"
        
        header = f"""SDD Version, SDDv2.0;
Software, SPT-SDD;
Author, Author;
Simulation Details, Nucleus simulation;
Source, Spectrum-driven;
Source type, 1;
Incident particles, {self.incident_pdg};
Mean particle energy, {mean_E:.6f};
Energy distribution, M, 0;
Particle fraction, 1.0;
Dose or fluence, {dose}, 1e-12;
Dose rate, {dose_rate};
Irradiation target, Nucleus;
Volumes, 0,5,5,5,0,0,0,1,4.65,4.65,4.65,0,0,0;
Chromosome sizes, 46,252.823,252.823,248.157,248.157,204.04,204.04,195.556,195.556,184.951,184.951,174.77,174.77,162.469,162.469,149.318,149.318,143.38,143.38,138.289,138.289,137.441,137.441,135.32,135.32,116.655,116.655,108.595,108.595,102.656,102.656,90.7788,90.7788,80.1738,80.1738,77.6286,77.6286,65.3268,65.3268,63.63,63.63,47.9346,47.9346,50.4798,50.4798,58.9638,158.227;
DNA Density, 14.4318;
Cell Cycle Phase, 0;
DNA Structure, 0, 1;
In vitro / in vivo, 0;
Proliferation status, 1;
Microenvironment, 20, 0.01;
Damage definition, 1, 0, 10, 10, 11.75;
Time, 0.000000;
Damage and primary count, {len(processed_body)}, {prims};
Data entries, {entries};
Additional information, ;
***EndOfHeader***;
"""
        
        with open(path, "w") as f:
            f.write(header)
            f.writelines(processed_body)