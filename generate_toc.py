import os
import re

root_dir = "internals-docs-code"
readme_path = os.path.join(root_dir, "index.md")

toc = ["# 📑 Data Engineering Knowledge Base\n"]

# Regex to strip numeric prefixes (like 01-, 02-)
prefix_pattern = re.compile(r"^\d+-")

def to_title_case(name: str) -> str:
    """Convert a cleaned filename or folder name into Title Case."""
    return " ".join(word.capitalize() for word in name.split())

def process_folder(folder_path, relative_path, level=2):
    """Recursively process a folder and add TOC entries."""
    folder_name = os.path.basename(folder_path)
    if folder_name.startswith(".") or folder_name.lower() in ["venv", ".github","notebooks"]:
        return

    # Section header (##, ###, etc. depending on depth)
    header_prefix = "#" * level
    toc.append(f"\n{header_prefix} {to_title_case(folder_name)}\n")

    # Collect files
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()

    for i, file in enumerate(files, start=1):
        name_raw = os.path.splitext(file)[0]
        name_clean = prefix_pattern.sub("", name_raw).replace("_", " ").replace("-", " ")
        name_title = to_title_case(name_clean)
        file_path = os.path.join(relative_path, file)
        toc.append(f"{i}. [{name_title}]({file_path})")

    # Process subdirectories
    subdirs = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    for subdir in sorted(subdirs):
        process_folder(os.path.join(folder_path, subdir), os.path.join(relative_path, subdir), level + 1)

# Start with all first-level subdirectories inside root_dir
for subdir in sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]):
    process_folder(os.path.join(root_dir, subdir), subdir)

new_toc = "\n".join(toc)

# Replace section in README.md between <!-- TOC START --> and <!-- TOC END -->
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- TOC START -->)(.*?)(<!-- TOC END -->)"
updated_content = re.sub(pattern, f"\\1\n{new_toc}\n\\3", readme_content, flags=re.DOTALL)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"✅ Updated {readme_path} with nested TOC")
