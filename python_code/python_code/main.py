import os
from modules.file_check_module import run_file_checks
from modules.data_quality_check_module import run_data_quality_checks

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def simulate_bad_files(input_dir):
    with open(os.path.join(input_dir, "invalid_file.txt"), "w") as f:
        f.write("Not a CSV.")
    with open(os.path.join(input_dir, "empty_file.csv"), "w") as f:
        pass

def main():
    input_dir = "input_files"
    output_dir = "output"
    processed_dir = "processed_files"
    bad_dir = "bad_files"

    ensure_dirs(input_dir, output_dir, processed_dir, bad_dir)

    print("Running file validation...")
    accepted_files = run_file_checks(input_dir) or []

    print(f"Accepted files for processing: {[os.path.basename(f) for f in accepted_files]}")

    print("Running data quality checks...")
    for file in accepted_files:
        run_data_quality_checks(file)

    print("Pipeline complete. Check 'output/' for results and 'bad_files/' for rejected files.")

if __name__ == "__main__":
    main()