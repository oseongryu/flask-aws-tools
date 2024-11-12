import csv
import os
from datetime import datetime

from dotenv import load_dotenv
from lxml import etree

load_dotenv()
export_path = os.getenv("sitemap_export_path")
# # URL 목록

# CSV 파일에서 URL 목록 읽기
urls = []
with open(os.path.expanduser("~") + "/urls.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 첫 번째 행(헤더)을 건너뜁니다.
    for row in reader:
        urls.append(row[0])  # 첫 번째 열의 값을 URL 목록에 추가


# # 오늘 날짜를 YYYY-MM-DD 형식으로 가져옵니다.
# last_change_date = datetime.now().strftime('%Y-%m-%d')
# '2024-10-03T18:00:26.843Z' 형식으로 날짜와 시간을 가져옵니다.
last_change_date = datetime.now().strftime("%Y-%m-%d")
# last_change_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

# XML 사이트맵 생성
urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for url in urls:
    url_element = etree.SubElement(urlset, "url")
    loc = etree.SubElement(url_element, "loc")
    loc.text = url
    lastmod = etree.SubElement(url_element, "lastmod")
    lastmod.text = last_change_date

# XML 문자열로 변환
sitemap = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="UTF-8")

# 사이트맵 파일로 저장
with open(export_path, "wb") as file:
    file.write(sitemap)

print("사이트맵이 생성되었습니다.")
