import boto3
import json
import decimal
import uuid
import time
import os
import gzip
import shutil
from dotenv import load_dotenv

from datetime import datetime
from slacker import Slacker
from apscheduler.schedulers.blocking import BlockingScheduler
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import json

load_dotenv()
region_name = os.getenv("REGION_NAME")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# pip install boto3
# pip install apscheduler
# pip install slacker
# CodeDeploy 클라이언트 생성
client = boto3.client("codedeploy", region_name=f"{region_name}", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")

# 배포 목록 가져오기
response = client.list_deployments()
deployments = response['deployments']

now = datetime.now()
now = datetime(now.year, now.month, now.day, 0, 0, 0)

def dateFormat(time, type = ''):
    if (type == 'ymd'):
        return time.strftime("%Y-%m-%d")
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
def post_message(channel, text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + SLACK_BOT_TOKEN
    }
    payload = {
        'channel': channel,
        'text': text
    }
    r = requests.post('https://slack.com/api/chat.postMessage',
                      headers=headers,
                      data=json.dumps(payload)
                      )


# print('--- {} deploy ----'.format(dateFormat(now, 'ymd')))
text_joined = '--- {} deploy ----'.format(dateFormat(now, 'ymd'))
for deployment_id in deployments:
  
    # 배포 상태 확인
    response = client.get_deployment(deploymentId=deployment_id)
    info = response['deploymentInfo']
    status = info.get('status')
    createTime = info.get('createTime')
    applicationName = info.get('applicationName')
    deploymentGroupName = info.get('deploymentGroupName')
    displaytime =dateFormat(createTime)
    target_time = createTime

    now_timestamp = now.timestamp()
    target_timestamp = target_time.timestamp()
    if now_timestamp < target_timestamp:
        result = "{} : {}, {}".format(deploymentGroupName.replace('hy-','').replace('-deploy-group', ''), displaytime, status )
        text_joined += "\n" + result
        # post_message("#passive-income", "{} : {}, {}".format(deploymentGroupName, displaytime, status ))
    else:
        break

post_message("#passive-income", text_joined)

    