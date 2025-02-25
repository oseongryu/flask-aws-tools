import os
import sys
from datetime import datetime, timedelta

import boto3
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import common.commonfunction as cmmfun

load_dotenv()
region_name = os.getenv("REGION_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

client = boto3.client("codedeploy", region_name=f"{region_name}", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")

response = client.list_deployments()
deployments = response["deployments"]
ex_targets = ["autoscaling"]


def run_deploy(search_dt):
    search_date = cmmfun.convert_string_to_datetime(search_dt)

    print("--- {} 배포상태 확인 ----".format(cmmfun.dateFormat(search_date, "ymd")))
    deploy_list = []
    for deployment_id in deployments:

        # 배포 상태 확인
        response = client.get_deployment(deploymentId=deployment_id)
        info = response["deploymentInfo"]
        creator = info.get("creator")
        status = info.get("status")
        createTime = info.get("createTime")
        # Convert createTime to UTC+9
        createTime = createTime + timedelta(hours=9)
        applicationName = info.get("applicationName")
        deploymentGroupName = info.get("deploymentGroupName")
        displaytime = cmmfun.dateFormat(createTime)
        target_time = createTime

        now_timestamp = search_date.timestamp()
        target_timestamp = target_time.timestamp()
        if now_timestamp < target_timestamp:
            if cmmfun.check_any_ex_targets_satisfied(creator, ex_targets) == False:
                print("{}: {}, {}".format(deploymentGroupName, displaytime, status))
                deploy_list.append({"deploymentGroupName": deploymentGroupName, "displaytime": displaytime, "status": status})
        else:
            break
    return deploy_list


if __name__ == "__main__":
    search_date = datetime.now() - timedelta(days=7)
    search_date_str = cmmfun.dateFormat(search_date, "ymd")
    run_deploy(search_date_str)
