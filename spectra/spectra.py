import os
from datetime import datetime


def get_file_metadata(filename):
    info = os.stat(filename)
    _, extension = os.path.splitext(filename)

    return {
        "name": os.path.basename(filename),
        "path": os.path.abspath(filename),
        "size": info.st_size,
        "modified": datetime.fromtimestamp(info.st_mtime),
        "created": datetime.fromtimestamp(info.st_ctime),
        "accessed": datetime.fromtimestamp(info.st_atime),
        "extension": extension.lower(),
    }
