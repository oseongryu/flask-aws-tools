import decimal
import gzip
import json
import os
import shutil
import time
import uuid

import boto3
from dotenv import load_dotenv


def lpad(i, width, fillchar="0"):
    return str(i).rjust(width, fillchar)


def rpad(i, width, fillchar="0"):
    return str(i).ljust(width, fillchar)


def make_folder(dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)


load_dotenv()
alb_was_path = os.getenv("ALB_WAS_PATH")
bucket = os.getenv("ALB_WAS_BUCKET")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

folderName = "was_log"
foldertime = "2025/03/27/"
folder = f"{alb_was_path}" + "/" + foldertime
localPath = os.path.expanduser("~") + "/" + folderName
# pip install boto3

make_folder(localPath)

# lists = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
lists = ["10"]
for hourIndex in lists:
    s3 = boto3.resource("s3", region_name="ap-northeast-2", aws_access_key_id=f"{aws_access_key_id}", aws_secret_access_key=f"{aws_secret_access_key}")
    s3bucket = s3.Bucket(bucket)
    s3objects = s3bucket.objects.filter(Prefix=folder + hourIndex).all()

    # s3objects = [obj.key for obj in sorted(s3objects, key=lambda x: x.last_modified, reverse=True)]
    def obj_last_modified(myobj):
        return myobj.last_modified

    sortedObjects = sorted(s3objects, key=obj_last_modified, reverse=False)
    cnt = 0
    for s3file in sortedObjects:
        cnt += 1
        filename = os.path.basename(s3file.key)
        filepath = s3file.key

        if "gz" in filepath:
            try:
                downLoad = localPath + "/" + folderName + "_" + foldertime.replace("/", "") + "_" + hourIndex + "_" + lpad(str(cnt), 2)
                s3bucket.download_file(filepath, downLoad + ".gz")
                with gzip.open(downLoad + ".gz", "rb") as f_in:
                    with open(downLoad, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(downLoad + ".gz")
                print("success: " + downLoad)
            except:
                print("fail : " + filename)

print("success finished")
