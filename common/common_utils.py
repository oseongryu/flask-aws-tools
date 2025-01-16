import os
import platform
from datetime import datetime

from models import FileModel


def convert_string_to_datetime(date_str):
    # Convert 'YYYY-MM-DD' string to datetime object
    return datetime.strptime(date_str, "%Y-%m-%d")


def check_all_targets_satisfied(line, targets):
    return all(condition in line for condition in targets)


def check_any_targets_satisfied(line, targets):
    return any(condition in line for condition in targets)


def check_any_ex_targets_satisfied(line, ex_targets):
    return any(condition in line for condition in ex_targets)


def dateFormat(time, type=""):
    if type == "ymd":
        return time.strftime("%Y-%m-%d")
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")


def add_user_home_path(value, use_yn):
    result = value
    if use_yn:
        result = os.path.expanduser("~") + value
    return result


def check():
    if is_windows():
        print("This is Windows")
    elif is_mac():
        print("This is Mac")
    elif is_unix():
        print("This is Unix or Linux")
    elif is_solaris():
        print("This is Solaris")
    else:
        print("Your OS is not supported!!")


def is_windows():
    os_name = platform.system().lower()
    return "windows" in os_name


def is_mac():
    os_name = platform.system().lower()
    return "darwin" in os_name


def is_unix():
    os_name = platform.system().lower()
    return "linux" in os_name or "aix" in os_name


def is_solaris():
    os_name = platform.system().lower()
    return "sunos" in os_name


def sub_full_path_list(original_file_dir, file_dir, result, type):
    file_separator = os.sep
    file_list = os.listdir(file_dir)
    for row_idx, file_name in enumerate(file_list):
        file_path = os.path.join(file_dir, file_name)
        if type == "dir":
            if os.path.isfile(file_path):
                continue
            elif os.path.isdir(file_path):
                parent_dir = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
                if not parent_dir == "app":
                    dto = FileModel(
                        file_id=row_idx,
                        file_name=file_name,
                        file_path=file_path,
                        file_dir=file_name,
                        file_parent_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        file_custom_dir=os.path.basename(os.path.dirname(file_path)) + file_separator + file_name,
                        depth1_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                        depth2_dir=os.path.basename(os.path.dirname(file_path)),
                        depth3_dir=file_name,
                    )
                    result.append(dto)
                sub_full_path_list(original_file_dir, os.path.realpath(file_path), result, type)
        else:
            if os.path.isfile(file_path):
                dto = FileModel(
                    file_id=row_idx,
                    file_name=file_name,
                    file_path=file_path,
                    file_dir=file_name,
                    file_parent_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                    file_custom_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))) + file_separator + os.path.basename(os.path.dirname(file_path)) + file_separator + file_name,
                    depth1_dir=os.path.basename(os.path.dirname(os.path.dirname(file_path))),
                    depth2_dir=os.path.basename(os.path.dirname(file_path)),
                    depth3_dir=file_name,
                )
                result.append(dto)
            elif os.path.isdir(file_path):
                sub_full_path_list(original_file_dir, os.path.realpath(file_path), result, type)
    return result
