from pathlib import Path
from typing import List, Dict
import re, os


def scan_directory(path: Path):
    """
    Recursively scan directories and follow symlinked folders/files.

    Returns:
        List[dict]: Indexed wordlist metadata
    """

    files = []

    for root, dirs, filenames in os.walk(path, followlinks=True):

        for filename in filenames:

            file_path = Path(root) / filename

            try:

                # Skip non-files
                if not file_path.is_file():
                    continue

                # Resolve symlinks to real canonical path
                resolved_path = file_path.resolve()

                # Extract tags from direcotry & filename
                tags = extract_tags(str(resolved_path))

                files.append({
                    "name": resolved_path.name,
                    "path": str(resolved_path),
                    "size": resolved_path.stat().st_size,
                    "mtime": int(resolved_path.stat().st_mtime),
                    "tags": ",".join(tags)
                })

            except Exception:
                # Skip unreadable/broken files safely
                continue

    return files


def extract_tags(file_path: str) -> list:
    """
    Extract simple tags from file path and filename.
    """

    parts = file_path.split("/")

    words = []

    for part in parts:

        # Remove common extension
        part = part.replace(".txt", "")

        # Split by separators
        split_words = re.split(r"[_\-\.]", part)

        for word in split_words:

            word = word.lower().strip()

            # Ignore very short words
            if len(word) > 2:
                words.append(word)

    # Remove duplicates and sort
    unique_words = sorted(set(words))

    return unique_words