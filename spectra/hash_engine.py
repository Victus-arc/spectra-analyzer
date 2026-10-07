import hashlib


def calculate_sha256(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def calculate_md5(filename):
    md5 = hashlib.md5()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            md5.update(chunk)

    return md5.hexdigest()


def calculate_sha1(filename):
    sha1 = hashlib.sha1()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            sha1.update(chunk)

    return sha1.hexdigest()


def calculate_blake2b(filename):
    blake2b = hashlib.blake2b()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            blake2b.update(chunk)

    return blake2b.hexdigest()


def calculate_hashes(filename):
    return {
        "MD5": calculate_md5(filename),
        "SHA-1": calculate_sha1(filename),
        "SHA-256": calculate_sha256(filename),
        "BLAKE2b": calculate_blake2b(filename),
    }
