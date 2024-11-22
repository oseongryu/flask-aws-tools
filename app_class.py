import os


class OriginInfoClass:
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
            back_sound_path=f"{base_url}/pythonapi/background/background-3.mp3",
            story_id=story_id,
            story_items=story_info_func(story_id),
            preview_image_path=f"{base_url}/pythonapi/shorts/{story_id}/1.webp",
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
            "storyId": self.storyId,
            "storyItems": self.storyItems,
            "previewImagePath": self.previewImagePath,
        }


class StoryClass:
    def __init__(self, seq, height, no, sound_path, image_path, prompt, content):
        self.seq = seq
        self.height = height
        self.no = no
        self.soundPath = sound_path
        self.imagePath = image_path
        self.prompt = prompt
        self.content = content

    @classmethod
    def from_row(cls, row_story, story_id):
        base_url = os.getenv("BASE_URL")
        image_path = row_story.get("image_path")
        sound_path = row_story.get("sound_path")
        # fmt: off
        return cls(
            seq=row_story.get("seq"),
            height=row_story.get("height"),
            no=row_story.get("no"),
            sound_path=f"{base_url}/pythonapi/shorts/{story_id}/{sound_path}",
            image_path=f"{base_url}/pythonapi/shorts/{story_id}/{image_path}",
            prompt=row_story.get("prompt"),
            content=row_story.get("content"),
        )
        # fmt: on

    def to_dict(self):
        return {
            "seq": self.seq,
            "height": self.height,
            "no": self.no,
            "soundPath": self.soundPath,
            "imagePath": self.imagePath,
            "prompt": self.prompt,
            "content": self.content,
        }


class PromptClass:
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


class PromptHistoryClass:
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
