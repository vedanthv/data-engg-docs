import os
import re
import yaml

BASE_DIR = "internals-docs-code"
SKIP_FOLDERS = {"notebooks"}  # folders to skip


def title_from_filename(filename: str) -> str:
    """
    Convert filename or folder into a pretty title.
    - Removes extension
    - Strips leading numbers and underscores/hyphens
    - Converts to Title Case
    """
    name = os.path.splitext(filename)[0]
    # Remove leading numbers like "01_", "02-", etc.
    name = re.sub(r"^\d+[_-]?", "", name)
    return name.replace("_", " ").replace("-", " ").title()


def generate_pages_yaml(folder: str, title: str) -> dict:
    """Generate .pages structure for a folder."""
    items = []

    entries = sorted(os.listdir(folder))
    # Ensure intro.md (or 00_intro.md, etc.) comes first
    entries.sort(key=lambda x: (not re.match(r"^(?:\d+[_-])?intro\.md$", x, re.IGNORECASE), x.lower()))

    for entry in entries:
        path = os.path.join(folder, entry)
        if entry.startswith("."):
            continue
        if os.path.isdir(path):
            if entry.lower() in SKIP_FOLDERS:
                continue
            items.append({title_from_filename(entry): entry + "/"})
        elif entry.endswith(".md"):
            items.append({title_from_filename(entry): entry})
    return {"title": title, "nav": items}


def write_pages_file(folder: str, title: str):
    """Write a .pages file in the given folder."""
    pages = generate_pages_yaml(folder, title)
    pages_file = os.path.join(folder, ".pages")
    with open(pages_file, "w", encoding="utf-8") as f:
        yaml.dump(pages, f, sort_keys=False, allow_unicode=True)


def process_folder(folder: str):
    """Process a folder recursively: write .pages for it and all subfolders."""
    title = title_from_filename(os.path.basename(folder)) if folder != BASE_DIR else "Internal Docs"
    write_pages_file(folder, title)

    for entry in os.listdir(folder):
        path = os.path.join(folder, entry)
        if os.path.isdir(path) and not entry.startswith(".") and entry.lower() not in SKIP_FOLDERS:
            process_folder(path)


def main():
    process_folder(BASE_DIR)


if __name__ == "__main__":
    main()
