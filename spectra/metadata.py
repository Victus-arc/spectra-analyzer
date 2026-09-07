import os
from datetime import datetime


def get_file_metadata(filename):
    info = os.stat(filename)

    return {
        "name": os.path.basename(filename),
        "size": info.st_size,
        "modified": datetime.fromtimestamp(info.st_mtime),
    }