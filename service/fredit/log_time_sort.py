import glob
import os
import posixpath
import re
from datetime import datetime

# 현재 날짜와 시간을 가져옵니다.
now = datetime.now()

targets = ["RSL_MSG=기타 오류"]
ex_targets = []

output_log_path = posixpath.join(os.path.expanduser("~"), "fredit_log")
output_file_name = now.strftime("%Y%m%d%H%M%S") + ".txt"
log_paths = [posixpath.join(output_log_path, f"was{i}") for i in range(1, 5)]


def check_all_targets_satisfied(line):
    # 모든 조건이 True인지 확인
    return all(condition in line for condition in targets)


def check_any_ex_targets_satisfied(line):
    return any(condition in line for condition in ex_targets)


# 로그 파일들에서 로그 라인을 추출
log_lines = []
for log_path in log_paths:

    # 로그 파일 경로 패턴
    log_files_pattern = log_path + "/*"

    # Regular expression to match the timestamp
    timestamp_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}")

    for log_file_path in sorted(glob.glob(log_files_pattern)):
        if "txt" not in log_file_path:
            with open(log_file_path, "r") as file:
                print(log_file_path)
                for line in file:

                    match = timestamp_pattern.match(line)
                    if match:
                        date_obj = datetime.strptime(line[:12], "%H:%M:%S.%f")
                        if check_any_ex_targets_satisfied(line) == False:
                            if check_all_targets_satisfied(line):
                                # line = line.split("fredit-token")[1].replace(": ", "")
                                log_lines.append((date_obj, line))


# 시간 순으로 로그 라인 정렬
log_lines.sort(key=lambda x: x[0])
print("sorted")
# 분석 결과를 저장할 파일 경로
output_file_path = posixpath.join(output_log_path, output_file_name)
# 정렬된 줄을 파일에 쓰기
with open(output_file_path, "w") as sorted_file:
    for _, line in log_lines:
        sorted_file.write(line)
