import glob
import os
from datetime import datetime
from multiprocessing import Pool
import random
import string

log_path = os.path.expanduser("~") + '/was_log'
log_files_pattern = log_path + '/*'
# targets = ["Googlebot", "detail?prdId="]
targets = ["aws-search-result"]

ex_targets = []

def check_all_targets_satisfied(line):
    return all(condition in line for condition in targets)


def check_any_ex_targets_satisfied(line):
    return any(condition in line for condition in ex_targets)

def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def process_log_files(file_paths):
    path = file_paths[0]
    basename = os.path.basename(path)  # Gets 'web_log_20241007_23_01'
    date_time_part = basename.split('_')[2:]  # Splits and takes the parts after 'web_log'
    date_time_str = '_'.join(date_time_part)  # Joins them back together

    log_lines = []
    for log_file_path in file_paths:
        with open(log_file_path, 'r') as file:
            for line in file:
                start_pos = line.find("http") + 4
                date_str = line[start_pos:].split()[0]
                date_obj = datetime.fromisoformat(date_str.rstrip("Z"))
                if (check_any_ex_targets_satisfied(line) == False):
                    if check_all_targets_satisfied(line):
                        log_lines.append((date_obj, line))
    # Sort log lines by date
    log_lines.sort(key=lambda x: x[0])
    # Write to a temporary file
    temp_file_name = f"temp_{os.getpid()}_{date_time_str}.txt"
    # temp_file_name = f"temp_{os.getpid()}_{generate_random_string()}.txt"
    print(temp_file_name, len(log_lines))
    with open(temp_file_name, 'w') as temp_file:
        for _, line in log_lines:
            temp_file.write(line)
    return temp_file_name

def combine_files(file_names):
    with open('log_sort_was.txt', 'w') as outfile:
        for fname in file_names:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
            os.remove(fname)  # Clean up temporary files

if __name__ == "__main__":
    log_files = sorted(glob.glob(log_files_pattern))
    # Group files by date prefix
    grouped_files = {}
    for log_file in log_files:
        date_prefix = os.path.basename(log_file)[:19]
        if date_prefix not in grouped_files:
            grouped_files[date_prefix] = []
        grouped_files[date_prefix].append(log_file)
    
    with Pool() as pool:
        temp_files = pool.map(process_log_files, grouped_files.values())
    
    combine_files(temp_files)