#!/usr/bin/python3

import os
import pathlib
import json
from dataclasses import dataclass
import logging
import argparse
import shutil
import hashlib



logging.basicConfig(level=logging.WARNING, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("Installer")

@dataclass
class ManifestEntry:
    path: pathlib.Path
    hash: str
    size: int

@dataclass
class PileEntry:
    path: str
    name: str
    size: int

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

def collect_files(path, pile):
    for element in os.scandir(path):
        if element.is_dir():
            collect_files(element.path, pile)
        else:
            file_hash = get_file_hash(element.path)
            file_size = element.stat().st_size
            pile[file_hash] = PileEntry(element.path, element.name, file_size)

def read_manifest(path):
    manifest = []
    with open(path, "r") as mf:
        for entry in json.load(mf):
            # Convert path to pathib object
            manifest.append(ManifestEntry(pathlib.Path(entry[0]), entry[1], entry[2]))
    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Install software files using a custom manifest format."
    )
    parser.add_argument("-m", "--manifest", type=str, required=True,
                        help="Manifest file that serves as a template for the installation.")
    parser.add_argument("-d", "--dest", type=pathlib.Path, required=True,
                        help="Install destination for the application.")
    parser.add_argument("-i", "--ignore-name", type=bool, default=False,
                        help="Ignore name matches if there is no hash match.")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Print more debug information")
    parser.add_argument("source", type=pathlib.Path, nargs="+",
                        help="Path to index for files, usually a CD/DVD mountpoint.")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    manifest = read_manifest(args.manifest)

    source_pile = {}
    for search_path in args.source:
        logger.info(f"Scanning {search_path}")
        collect_files(search_path, source_pile)

    copy_tasks = []
    for file_entry in manifest:
        match_type = None
        hash_match = source_pile.get(file_entry.hash)
        if hash_match is not None:
            logger.info(f"Hash match {file_entry.path}: {hash_match.path}")
            copy_tasks.append((file_entry.path, hash_match.path))
        else:
            name_matches = []
            if not args.ignore_name:
                target_fn = file_entry.path.name
                for pile_entry in source_pile.values():
                    if pile_entry.name == target_fn:
                        size_diff = abs(file_entry.size - pile_entry.size)
                        name_matches.append((pile_entry, size_diff))
                name_matches.sort(key=lambda x: x[1]) # sort by size diff
            if name_matches:
                logger.info(f"Found {len(name_matches)} name matches:")
                for i, nm in enumerate(name_matches):
                    logger.info(f"  [{i}] {nm[0].path}")
                chosen_nm = name_matches[0][0]
                logger.warning(f"No hash match found for {file_entry.path}, using name match: {chosen_nm.path}")
                copy_tasks.append((file_entry.path, chosen_nm.path))
            else:
                logger.error(f"NO MATCH! {file_entry.path}")

    for dest, src in copy_tasks:
        if dest.is_absolute():
            dest = dest.relative_to("/")
        install_dest = args.dest / dest
        logger.info(f"Copying {src} -> {dest}")
        os.makedirs(install_dest.parent, exist_ok=True)
        shutil.copyfile(src, install_dest)

if __name__ == "__main__":
    main()
