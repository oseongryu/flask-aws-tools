from flask import Blueprint, current_app, jsonify, request

from models import OriginInfoModel, PromptModel, PromptHiStoryModel, StoryModel
from services import (
    delete_origin_info,
    delete_story,
    insert_origin_info,
    insert_story,
    max_origin_info_seq,
    max_story_seq,
    select_origin_info,
    select_prompt,
    select_prompt_history,
    select_table,
    update_origin_info,
)
from auth import token_required

routes_shorts = Blueprint("routes_shorts", __name__)


@routes_shorts.route("/api/origin-info/search-origin-info", methods=["POST"])
@token_required
def query_origin_info():
    try:
        request_data = request.get_json()
        storyId = request_data.get("storyId")
        return jsonify(select_origin_info(storyId)), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/origin-info/search-origin-info-list", methods=["POST"])
@token_required
def query_origin_info_list():
    try:
        return jsonify(select_origin_info("")), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/origin-info/save-origin-info", methods=["POST"])
@token_required
def query_save_origin_info():
    try:
        request_data = request.get_json()
        content = request_data.get("content")
        originContent = request_data.get("originContent")
        originTitle = request_data.get("originTitle")
        originUrl = request_data.get("originUrl")
        title = request_data.get("title")

        storyId = request_data.get("storyId")
        if storyId and len(select_origin_info(storyId)) == 1:
            update_origin_info(storyId, content, originContent, originTitle, originUrl, title)
        else:
            storyId = max_origin_info_seq()
            insert_origin_info(storyId, content, originContent, originTitle, originUrl, title)
        return jsonify({}), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/origin-info/delete-origin-info", methods=["POST"])
@token_required
def query_delete_origin_info():
    try:
        request_data = request.get_json()
        storyId = request_data.get("storyId")
        if storyId and len(select_origin_info(storyId)) == 1:
            delete_story(storyId)
            delete_origin_info(storyId)
        return jsonify({}), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/origin-info/save-story", methods=["POST"])
@token_required
def query_save_story():
    try:
        request_data = request.get_json()
        storyId = request_data.get("storyId")
        storyItems = request_data.get("storyItems")
        delete_story(storyId)
        max_seq = max_story_seq(storyId)
        for idx, storyItem in enumerate(storyItems, 1):
            insert_story(storyId, max_seq + idx, str(idx), storyItem)
        return jsonify({}), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/prompt", methods=["GET"])
@token_required
def query_prompt():
    try:
        return jsonify(select_table("prompt", "PromptModel")), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500


@routes_shorts.route("/api/prompt-history", methods=["GET"])
@token_required
def query_prompt_history():
    try:
        return jsonify(select_table("prompt_history", "PromptHiStoryModel")), 200
    except Exception as e:
        return jsonify(message=f"Error: {str(e)}"), 500
