import os


class FileModel:
    # fmt: off
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
