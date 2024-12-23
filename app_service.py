from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from app_class import OriginInfoClass, PromptClass, PromptHistoryClass, StoryClass


def select_origin_info(storyId):
    query = "SELECT * FROM origin_info"
    if storyId != "":
        query = f"SELECT * FROM origin_info WHERE story_id = {storyId}"
    class_name = OriginInfoClass.__name__
    return fetch_and_transform(query, class_name, "")


def select_story(storyId):
    class_name = StoryClass.__name__
    query = f"SELECT * FROM story WHERE story_id = {storyId}"
    return fetch_and_transform(query, class_name, storyId)


def select_prompt():
    class_name = PromptClass.__name__
    table_name = "prompt"
    query = f"SELECT * FROM {table_name}"
    return fetch_and_transform(query, class_name, "")


def select_prompt_history():
    class_name = PromptHistoryClass.__name__
    table_name = "prompt_history"
    query = f"SELECT * FROM {table_name}"
    return fetch_and_transform(query, class_name, "")


def select_table(table_name, class_name):
    class_name = globals()[class_name].__name__
    query = f"SELECT * FROM {table_name}"
    return fetch_and_transform(query, class_name, "")


def insert_origin_info(storyId, content, originContent, originTitle, originUrl, title):
    cur = current_app.db.cursor()
    user = "admin"
    created_date = modified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(
        "INSERT INTO origin_info (story_id, content, origin_content, origin_title, origin_url, title, created_by, created_date, modified_by, modified_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (storyId, content, originContent, originTitle, originUrl, title, user, created_date, user, modified_date),
    )
    current_app.db.commit()
    cur.close()
    return {"msg": "success"}


def update_origin_info(storyId, content, originContent, originTitle, originUrl, title):
    cur = current_app.db.cursor()
    user = "admin"
    modified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        "UPDATE origin_info SET modified_by=?, modified_date=?, content=?, origin_content=?, origin_title=?, origin_url=?, title=? WHERE story_id=?", 
        (user, modified_date, content, originContent, originTitle, originUrl, title, storyId)
    )
    current_app.db.commit()
    cur.close()
    return {"msg": "success"}


def delete_origin_info(storyId):
    cur = current_app.db.cursor()
    cur.execute("DELETE FROM origin_info WHERE story_id = ?", (storyId,))
    current_app.db.commit()
    cur.close()
    return {"msg": "success"}


def insert_story(storyId, seq, idx, storyItem):
    cur = current_app.db.cursor()
    user = "admin"
    height = storyItem.get("height")
    no = idx
    soundPath = f"{idx}.mp3"
    imagePath = f"{idx}.webp"
    content = storyItem.get("content")
    created_date = modified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(
        "INSERT INTO story (story_id, id, height, no, sound_path, image_path, content, created_by, created_date, modified_by, modified_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (storyId, seq, height, no, soundPath, imagePath, content, user, created_date, user, modified_date),
    )
    current_app.db.commit()
    cur.close()
    return {"msg": "success"}


def max_origin_info_seq():
    cur = current_app.db.cursor()
    cur.execute("SELECT MAX(story_id) seq FROM origin_info")
    rows = cur.fetchall()
    description = cur.description
    cur.close()

    column_names = [desc[0] for desc in description]
    result = [dict(zip(column_names, row)) for row in rows]
    val = 0
    if result[0].get("seq") == None:
        val = 1
    else:
        val = result[0].get("seq") + 1
    return val


def max_story_seq(storyId):
    cur = current_app.db.cursor()
    cur.execute("SELECT MAX(id) seq FROM story")
    rows = cur.fetchall()
    description = cur.description
    cur.close()

    column_names = [desc[0] for desc in description]
    result = [dict(zip(column_names, row)) for row in rows]
    val = 0
    if result[0].get("seq") == None:
        val = 1
    else:
        val = result[0].get("seq")
    return val


# def delete_origin_info(storyId):
#     cur = current_app.db.cursor()
#     delete_query = f"DELETE FROM origin_info WHERE = {storyId}"
#     cur.execute(delete_query)
#     current_app.db.commit()
#     cur.close()
#     return {'msg': 'success'}


def delete_story(storyId):
    cur = current_app.db.cursor()
    cur.execute("DELETE FROM story WHERE story_id = ?", (storyId,))
    current_app.db.commit()
    cur.close()
    return {"msg": "success"}


def fetch_and_transform(query, class_name, story_id):
    transform_class = globals()[class_name]
    cur = current_app.db.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    description = cur.description
    cur.close()

    column_names = [desc[0] for desc in description]
    result = [dict(zip(column_names, row)) for row in rows]
    if class_name == "OriginInfoClass":
        transformed_result = [transform_class.from_row(row, row.get("story_id"), select_story).to_dict() for row in result]
    elif class_name == "StoryClass":
        transformed_result = [transform_class.from_row(row, story_id).to_dict() for row in result]
    elif class_name == "PromptClass":
        transformed_result = [transform_class.from_row(row).to_dict() for row in result]
    elif class_name == "PromptHistoryClass":
        transformed_result = [transform_class.from_row(row).to_dict() for row in result]
    return transformed_result
