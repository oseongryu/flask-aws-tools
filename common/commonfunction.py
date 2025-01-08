# -*- coding: utf-8 -*-
import gzip
import os
import shutil
import subprocess
import time

# pip install psutil
import psutil
import requests


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
