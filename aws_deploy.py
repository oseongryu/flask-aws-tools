import decimal
import gzip
import json
import os
import shutil
import time
import uuid
from datetime import datetime

import boto3
from dotenv import load_dotenv

load_dotenv()
region_name = os.getenv("region_name")
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")

client = boto3.client("codedeploy", region_name=f"{region_name}", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")

response = client.list_deployments()
deployments = response["deployments"]
ex_targets = ["autoscaling"]


def convert_string_to_datetime(date_str):
    # Convert 'YYYY-MM-DD' string to datetime object
    return datetime.strptime(date_str, "%Y-%m-%d")


def check_any_ex_targets_satisfied(line):
    return any(condition in line for condition in ex_targets)


def dateFormat(time, type=""):
    if type == "ymd":
        return time.strftime("%Y-%m-%d")
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")


def run_deploy(search_dt):
    search_date = convert_string_to_datetime(search_dt)

    print("--- {} 배포상태 확인 ----".format(dateFormat(search_date, "ymd")))
    deploy_list = []
    for deployment_id in deployments:

        # 배포 상태 확인
        response = client.get_deployment(deploymentId=deployment_id)
        info = response["deploymentInfo"]
        creator = info.get("creator")
        status = info.get("status")
        createTime = info.get("createTime")
        applicationName = info.get("applicationName")
        deploymentGroupName = info.get("deploymentGroupName")
        displaytime = dateFormat(createTime)
        target_time = createTime

        now_timestamp = search_date.timestamp()
        target_timestamp = target_time.timestamp()
        if now_timestamp < target_timestamp:
            if check_any_ex_targets_satisfied(creator) == False:
                print("{}: {}, {}".format(deploymentGroupName, displaytime, status))
                deploy_list.append({"deploymentGroupName": deploymentGroupName, "displaytime": displaytime, "status": status})
        else:
            break
    return deploy_list


if __name__ == "__main__":
    search_date = convert_string_to_datetime("20241029")
    run_deploy(search_date)
