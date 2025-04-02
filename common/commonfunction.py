# -*- coding: utf-8 -*-
import gzip
import os
import platform
import re
import shutil
import subprocess
import time
from datetime import datetime

# pip install psutil
import psutil
import requests

from module_common.models import FileModel

AUTO_ROOT = "automation"


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(word):
    components = word.split("_")
    return components[0] + "".join(x.capitalize() for x in components[1:])


def lpad(i, width, fillchar="0"):
    return str(i).rjust(width, fillchar)


def rpad(i, width, fillchar="0"):
    return str(i).ljust(width, fillchar)


def check_boolean(value):
    result = False
    if value == "False":
        result = False
    else:
        result = True
    return result


def isRetina():
    if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell=True) == 0:
        IS_RETINA = True
        return IS_RETINA


def make_folder(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)


def decrypt_text(value):
    # fernet = Fernet(bytes(utils.KEY,'utf-8'))
    # VALUE = fernet.decrypt(bytes(value,'utf-8')).decode()
    return ""
    # return VALUE


def split_value(value):
    if value is not None:
        split = value.split("=", maxsplit=1)
        if len(split) == 2:
            return split[0], split[1]
    return None, None


def get_processes(processName):
    chrome_processes = []
    for process in psutil.process_iter(attrs=["pid", "name"]):
        if processName in process.info["name"].lower():
            chrome_processes.append(process.info["pid"])
    return chrome_processes


def check_process_port(num):
    target_port = num
    chk_port = True
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == target_port:
                    print(f"Process ID: {proc.info['pid']}, Process Name: {proc.info['name']} is using port {target_port}")
                    chk_port = False
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return chk_port


def kill_processes(processName):
    chrome_pids = get_processes(processName)
    for pid in chrome_pids:
        try:
            p = psutil.Process(pid)
            p.terminate()  # or p.kill() if terminate does not work
        except psutil.NoSuchProcess:
            pass  # Process might have already been terminated


# 파일 다운로드 함수
def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return local_filename


# .gz 파일 압축 해제 함수
def decompress_gz(gz_filename, decompressed_filename):
    with gzip.open(gz_filename, "rb") as f_in:
        with open(decompressed_filename, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def add_user_home_path(value, use_yn):
    result = value
    if use_yn:
        result = os.path.expanduser("~") + value
    return result


def img_copy():
    import pyautogui

    pyautogui.hotkey("ctrl", "s", interval=0.1)
    print("1111")
    time.sleep(5)
    pyautogui.typewrite("temp", interval=0.1)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(10)
    import subprocess

    user = os.path.expanduser("~")
    make_folder(os.path.expanduser("~") + "/Downloads/temp")
    command = f"cd {user}/Downloads && cp -r ./temp_files/*.webp ./temp  && rm -rf ./temp.html && rm -rf ./temp_files"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode())


def keyboard_enter():
    import pyautogui

    time.sleep(2)
    pyautogui.press("enter")


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
                if not parent_dir == AUTO_ROOT:
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
