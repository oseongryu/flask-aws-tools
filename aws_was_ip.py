import decimal
import gzip
import json
import os
import shutil
import subprocess
import time
import uuid

import boto3
from dotenv import load_dotenv

load_dotenv()
region_name = os.getenv("region_name")
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")

ec2 = boto3.resource("ec2", region_name=f"{region_name}", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")

targets = ["-dev", "-prd"]
ex_targets = ["asg01", "compute", "arn", "bastion", "relay", "git", "api"]


def check_all_targets_satisfied(line):
    return all(condition in line for condition in targets)


def check_any_targets_satisfied(line):
    return any(condition in line for condition in targets)


def check_any_ex_targets_satisfied(line):
    return any(condition in line for condition in ex_targets)


def check_instance_exist(ec2):
    instances = ec2.instances.all()
    ec2_check = False
    for instance in instances:
        print(f"ec2 instance(type:{instance} is exist")
    return ec2_check


def run_aws_ip():
    arrdev = []
    arrprd = []

    instances = ec2.instances.filter(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])

    for instance in instances:
        try:
            tags = instance.tags
            for tag in tags:
                value = tag["Value"]
                if check_any_ex_targets_satisfied(value) == False and check_any_targets_satisfied(value):
                    if "dev" in value:
                        arrdev.append(value + ":" + instance.private_ip_address)
                    elif "prd" in value:
                        arrprd.append(value + ":" + instance.private_ip_address)
        except Exception as e:
            print(e)

    print("--- dev ---")
    sorted(arrdev)
    arrdev.sort()
    for item in arrdev:
        print(item)

    print("--- prd ---")
    arrprd.sort()
    for item in arrprd:
        print(item)
    return arrdev, arrprd


if __name__ == "__main__":
    run_aws_ip()
