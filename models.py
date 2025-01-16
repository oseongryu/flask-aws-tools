import os


class OriginInfoModel:
    def __init__(self, origin_url, origin_title, origin_content, title, content, back_sound_path, story_id, story_items, preview_image_path):
        self.originUrl = origin_url
        self.originTitle = origin_title
        self.originContent = origin_content
        self.title = title
        self.content = content
        self.backSoundPath = back_sound_path
        self.storyId = story_id
        self.storyItems = story_items
        self.previewImagePath = preview_image_path

    @classmethod
    def from_row(cls, row, story_id, story_info_func):
        base_url = os.getenv("BASE_URL")
        # fmt: off
        return cls(
            origin_url=row.get("origin_url"),
            origin_title=row.get("origin_title"),
            origin_content=row.get("origin_content"),
            title=row.get("title"),
            content=row.get("content"),
            back_sound_path=f"{base_url}/shorts/background/background-3.mp3",
            story_id=story_id,
            story_items=story_info_func(story_id),
            preview_image_path=f"{base_url}/shorts/{story_id}/1.webp",
        )
        # fmt: on

    def to_dict(self):
        return {
            "originUrl": self.originUrl,
            "originTitle": self.originTitle,
            "originContent": self.originContent,
            "title": self.title,
            "content": self.content,
            "backSoundPath": self.backSoundPath,
            "storyId": str(self.storyId),
            "storyItems": self.storyItems,
            "previewImagePath": self.previewImagePath,
        }


class StoryModel:
    def __init__(self, seq, height, no, sound_paths, image_path, prompt, content):
        self.seq = seq
        self.height = height
        self.no = no
        self.soundPaths = sound_paths
        self.imagePath = image_path
        self.prompt = prompt
        self.content = content

    @classmethod
    def from_row(cls, row_story, story_id):
        base_url = os.getenv("BASE_URL")
        image_path = row_story.get("image_path")
        no = row_story.get("no")
        content_list = row_story.get("content").split("\n")
        soundPaths = [(f"{base_url}/shorts/" + str(story_id) + "/" + f"{str(no)}{str(index + 1)}.mp3") for index, _ in enumerate(content_list)]

        # fmt: off
        return cls(
            seq=row_story.get("seq"),
            height=row_story.get("height"),
            no=row_story.get("no"),
            sound_paths=soundPaths,
            image_path=f"{base_url}/shorts/{story_id}/{image_path}",
            prompt=row_story.get("prompt"),
            content=row_story.get("content"),
        )
        # fmt: on

    def to_dict(self):
        return {
            "seq": self.seq,
            "height": self.height,
            "no": self.no,
            "soundPaths": self.soundPaths,
            "imagePath": self.imagePath,
            "prompt": self.prompt,
            "content": self.content,
        }


class PromptModel:
    def __init__(self, id, user_text, assistant_text, prompt_text, image_path):
        self.id = id
        self.userText = user_text
        self.assistantText = assistant_text
        self.promptText = prompt_text
        self.imagePath = image_path

    @classmethod
    def from_row(cls, row):
        # fmt: off
        return cls(
            id=row.get("id"),
            user_text=row.get("user_text"),
            assistant_text=row.get("assistant_text"),
            prompt_text=row.get("prompt_text"),
            image_path=row.get("image_path")
        )
        # fmt: on

    def to_dict(self):
        return {
            "id": self.id,
            "userText": self.userText,
            "assistantText": self.assistantText,
            "promptText": self.promptText,
            "imagePath": self.imagePath,
        }


class PromptHiStoryModel:
    def __init__(self, id, progress_status, user_text, story_id):
        self.id = id
        self.progressStatus = progress_status
        self.userText = user_text
        self.storyId = story_id

    @classmethod
    def from_row(cls, row):
        # fmt: off
        return cls(
            id=row.get("id"),
            progress_status=row.get("progress_status"),
            user_text=row.get("user_text"),
            story_id=row.get("story_id")
        )
        # fmt: on

    def to_dict(self):
        return {
            "id": self.id,
            "progressStatus": self.progressStatus,
            "userText": self.userText,
            "storyId": self.storyId,
        }


class FileModel:
    def __init__(self, file_id, file_name, file_path, file_dir, file_parent_dir, file_custom_dir, depth1_dir, depth2_dir, depth3_dir):
        self.file_id = file_id
        self.file_name = file_name
        self.file_path = file_path
        self.file_dir = file_dir
        self.file_parent_dir = file_parent_dir
        self.file_custom_dir = file_custom_dir
        self.depth1_dir = depth1_dir
        self.depth2_dir = depth2_dir
        self.depth3_dir = depth3_dir

    def to_dict(self):
        return {
            "fileId": self.file_id,
            "fileName": self.file_name,
            "filePath": self.file_path,
            "fileDir": self.file_dir,
            "fileParentDir": self.file_parent_dir,
            "fileCustomDir": self.file_custom_dir,
            "depth1Dir": self.depth1_dir,
            "depth2Dir": self.depth2_dir,
            "depth3Dir": self.depth3_dir,
        }
