import decimal
import gzip
import json
import os
import shutil
import subprocess
import sys
import time
import uuid

import boto3
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))
import common.common_utils as utils

load_dotenv()
region_name = os.getenv("REGION_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

ec2 = boto3.resource("ec2", region_name=f"{region_name}", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")

targets = ["-dev", "-prd"]
ex_targets = ["asg01", "compute", "arn", "relay", "git01"]


def check_instance_exist(ec2):
    instances = ec2.instances.all()
    ec2_check = False
    for instance in instances:
        print(f"ec2 instance(type:{instance} is exist")
    return ec2_check


def run_aws_ip():
    arr_list = []

    instances = ec2.instances.filter(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])

    for instance in instances:
        try:
            tags = instance.tags
            for tag in tags:
                value = tag["Value"]
                if utils.check_any_ex_targets_satisfied(value, ex_targets) == False and utils.check_any_targets_satisfied(value, targets):
                    arr_list.append({"name": value, "ip": instance.private_ip_address})
        except Exception as e:
            print(e)

    print("--- list ---")
    sorted_list = sorted(arr_list, key=lambda x: x["name"])
    for item in sorted_list:
        print(item)

    return sorted_list


if __name__ == "__main__":
    run_aws_ip()
