## pycache

```bash
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

## ER-Diagram

```mermaid
erDiagram
    origin_info ||--o{ story : ""
    origin_info ||--o{ sound_history : ""
    origin_info ||--o{ prompt_history : ""

    origin_info {
      string story_id
      string content
      string origin_content
      string origin_title
      string origin_url
      string title
    }
    prompt {
      string id
      string assistant_text
      string image_path
      string prompt_text
      string user_text
    }
    prompt_history {
      string id
      string progress_status
      string user_text
      string story_id
    }
    sound_history {
      string id
      string no
      string play_id
      string speak_url
      string speak_v2_url
      string story_id
    }
    story {
      string id
      string content
      string height
      string image_path
      string no
      string sound_path
      string story_id
    }
```

### Flask

```bash
python -m venv venv
# windows
source venv/Scripts/activate
# mac
source venv/bin/activate

# setting
python -m pip install --upgrade pip
pip freeze > requirements.txt
pip install -r requirements.txt

pip install --upgrade pip
pip install Flask
pip install python-dotenv
pip install pyjwt
pip install pillow
pip install psutil
pip install requests
pip install boto3
pip install mysqlclient
pip install Flask-MySQLdb
pip install mysql-connector-python
pip install flask_sqlalchemy
pip install pymysql
# 암호화 사용시
pip install cryptography

# mac
## mysql_native_password.so' (no such file)
brew install mysql pkg-config
brew uninstall mysql
brew install mysql@8.4

# Linux (Ubuntu)
apt-get install -y pkg-config python-dev default-libmysqlclient-dev libssl-dev
sudo apt-get install scrot
```

### docker-compose.yml

```bash
cd docker
curl -o docker-compose.yml https://raw.githubusercontent.com/oseongryu/docker-composes/refs/heads/main/automation/docker-compose.yml
cd desktop
curl -o Dockerfile https://raw.githubusercontent.com/oseongryu/docker-composes/refs/heads/main/automation/desktop/Dockerfile
docker-compose up --build -d desktop
```

## exec file (windows)

```bash
pip install pyinstaller
pyinstaller -w -F automation.py
```

## exec file (mac)

```bash
pip install py2app

py2applet --make-setup commonconverter.py
rm -rf build dist
python setup.py py2app -A
```

## references

```
https://py2app.readthedocs.io/en/latest/tutorial.html#building-for-deployment
```

```
https://raw.githubusercontent.com/oseongryu/til/refs/heads/main/public/img/android/001.png
```
