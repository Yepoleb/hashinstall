#!/usr/bin/python3
import json
import pathlib
import argparse
import hashlib



BLOCK_SIZE = 1024**2

def get_file_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(BLOCK_SIZE)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def collect_files_dest(path):
    file_list = []
    for child_path in path.glob("**/*"):
        if child_path.is_file():
            file_hash = get_file_hash(child_path)
            file_size = child_path.stat().st_size
            file_list.append([str(child_path.relative_to(path)), file_hash, file_size])
    return file_list

def main():
    parser = argparse.ArgumentParser(
        description="Generate manifest files to use with a special install script."
    )
    parser.add_argument("source", type=pathlib.Path,
                        help="Path to index for files, this should be a clean installation.")
    parser.add_argument("-m", "--manifest", type=str, required=True,
                        help="Manifest file to write.")
    args = parser.parse_args()

    file_list = collect_files_dest(args.source)
    with open(args.manifest, "w") as mf:
        json.dump(file_list, mf, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
