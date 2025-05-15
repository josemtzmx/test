import os
import shutil

PROCESSED_DIR = 'processed_files'
BAD_DIR = 'bad_files'

def is_new_file(filename, processed_files):
    return filename not in processed_files

def is_csv(filename):
    return filename.endswith('.csv')

def is_not_empty(filepath):
    return os.path.getsize(filepath) > 0

def run_file_checks(input_dir):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(BAD_DIR, exist_ok=True)

    processed_files = set(os.listdir(PROCESSED_DIR))
    accepted_files = []

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not is_csv(filename):
            shutil.move(filepath, os.path.join(BAD_DIR, filename))
        elif not is_not_empty(filepath):
            shutil.move(filepath, os.path.join(BAD_DIR, filename))
        elif filename in processed_files:
            shutil.move(filepath, os.path.join(BAD_DIR, filename))
        else:
            shutil.copy(filepath, os.path.join(PROCESSED_DIR, filename))
            accepted_files.append(filepath)

    return accepted_files