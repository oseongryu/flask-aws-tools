### Flask 실행

```bash
flask run

# 확인
http://127.0.0.1:8091/aws/
```


### flow

```mermaid
  info
```

```mermaid
flowchart LR
    1["http://localhost:8091/automation/python-exec?id=0"]
    2["http://localhost:8092/automation/python-exec?id=1"]
    3["http://localhost:8093/automation/python-exec?id=2"]
    4["http://localhost:8094/automation/python-exec?id=3"]
    5["http://localhost:8095/automation/python-exec?id=4"]

    click 1 "http://localhost:8091/automation/python-exec?id=0"
    click 2 "http://localhost:8092/automation/python-exec?id=1"
    click 3 "http://localhost:8093/automation/python-exec?id=2"
    click 4 "http://localhost:8094/automation/python-exec?id=3"
    click 5 "http://localhost:8095/automation/python-exec?id=4"

```

### ZenUML

```mermaid
zenuml
    title user
    @Actor user
    @EC2 ec2
    @Database db

    user->ec2: Hi Bob
    ec2->db: Hi Alice

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

## setting
```bash
python -m venv venv
# windows
source venv/Scripts/activate
# mac
source venv/bin/activate

# linumx
sudo apt-get install scrot


pip install --upgrade pip
pip install pyautogui
pip install selenium
pip install webdriver_manager
pip install pillow
pip install opencv-python
pip install fake-useragent
pip install psutil
```

## setup

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
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
https://py2app.readthedocs.io/en/latest/tutorial.html#building-for-deployment


### Flask

```bash

python -m venv venv
# windows
source venv/Scripts/activate
# mac
source venv/bin/activate

# mac
brew install mysql pkg-config
pip install mysqlclient

# Linux (Ubuntu)
apt-get install -y pkg-config python-dev default-libmysqlclient-dev libssl-dev 

pip install --upgrade pip
pip install Flask
pip install Flask-MySQLdb
pip install python-dotenv
pip install mysql-connector-python
pip install gTTS
touch .flaskenv

flask run
```


