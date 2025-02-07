import glob
import os
import re
from datetime import datetime

targets = ["Googlebot", "detail?prdId="]
ex_targets = ["utm_source=", "platform=ad"]
log_path = os.path.expanduser("~") + "/web_log"

# 로그 파일 경로 패턴
log_files_pattern = log_path + "/*"


# 모든 target 조건을 만족하는지 확인하는 함수
def check_all_targets_satisfied(line):
    # 모든 조건이 True인지 확인
    return all(condition in line for condition in targets)


def check_any_ex_targets_satisfied(line):
    return any(condition in line for condition in ex_targets)


# 로그 파일들에서 로그 라인을 추출
log_lines = []
for log_file_path in sorted(glob.glob(log_files_pattern)):
    if "txt" not in log_file_path:
        with open(log_file_path, "r") as file:
            print(log_file_path)
            for line in file:
                # 날짜와 시간을 추출하기 위한 시작 부분 찾기
                start_pos = line.find("http") + 4
                # 공백으로 구분된 첫 번째 부분이 날짜와 시간
                date_str = line[start_pos:].split()[0]

                # 'Z'를 제거하고 datetime 객체로 변환
                date_obj = datetime.fromisoformat(date_str.rstrip("Z"))
                # print(date_obj)
                if check_any_ex_targets_satisfied(line) == False:
                    if check_all_targets_satisfied(line):
                        # 시간 문자열을 datetime 객체로 변환
                        # log_datetime = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
                        log_lines.append((date_obj, line))
                    # # IP와 시간을 추출하기 위한 정규 표현식 예시
                    # match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                    # if match:
                    #     log_time = match.group(1)


# 시간 순으로 로그 라인 정렬
log_lines.sort(key=lambda x: x[0])
print("sorted")
# 분석 결과를 저장할 파일 경로
output_file_path = f"{log_path}/log_sort_web.txt"
# 정렬된 줄을 파일에 쓰기
with open(output_file_path, "w") as sorted_file:
    for _, line in log_lines:
        sorted_file.write(line)
