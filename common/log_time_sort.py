import glob
import os
import re
from datetime import datetime

# 타겟 설정
target = "result"
targets = ["userId: test"]
ex_targets = []

log_paths = [os.path.expanduser("~") + "/fredit_log/was1", os.path.expanduser("~") + "/fredit_log/was2", os.path.expanduser("~") + "/fredit_log/was3", os.path.expanduser("~") + "/fredit_log/was4"]
output_log_path = os.path.expanduser("~") + "/fredit_log"
# 로그 파일들에서 로그 라인을 추출
log_lines = []
for log_path in log_paths:

    # 로그 파일 경로 패턴
    log_files_pattern = log_path + "/*"

    # 모든 target 조건을 만족하는지 확인하는 함수
    def check_all_targets_satisfied(line):
        # 모든 조건이 True인지 확인
        return all(condition in line for condition in targets)

    def check_any_ex_targets_satisfied(line):
        return any(condition in line for condition in ex_targets)

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
output_file_path = "{}/result_{}.txt".format(output_log_path, target)
# 정렬된 줄을 파일에 쓰기
with open(output_file_path, "w") as sorted_file:
    for _, line in log_lines:
        sorted_file.write(line)
