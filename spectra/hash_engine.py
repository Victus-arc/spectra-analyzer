import hashlib


def _hash_file(filename, algorithm):
    digest = hashlib.new(algorithm)

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            digest.update(chunk)

    return digest.hexdigest()


def calculate_sha256(filename):
    return _hash_file(filename, "sha256")


def calculate_md5(filename):
    return _hash_file(filename, "md5")


def calculate_sha1(filename):
    return _hash_file(filename, "sha1")


def calculate_blake2b(filename):
    return _hash_file(filename, "blake2b")


def calculate_hashes(filename):
    return {
        "MD5": calculate_md5(filename),
        "SHA-1": calculate_sha1(filename),
        "SHA-256": calculate_sha256(filename),
        "BLAKE2b": calculate_blake2b(filename),
    }
