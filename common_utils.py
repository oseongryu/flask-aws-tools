from datetime import datetime


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
