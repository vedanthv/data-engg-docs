import os
import re

root_dir = "internals-docs-code"
readme_path = os.path.join(root_dir, "README.md")

toc = ["# 📑 Table of Contents\n"]

# Regex to strip numeric prefixes (like 01-, 02-)
prefix_pattern = re.compile(r"^\d+-")

def to_title_case(name: str) -> str:
    """Convert a cleaned filename or folder name into Title Case."""
    return " ".join(word.capitalize() for word in name.split())

# Collect all folder names (recursively)
all_folders = []
top_level_folders = []
for current_dir, subdirs, files in os.walk(root_dir):
    if current_dir == root_dir:
        continue
    folder_name = os.path.basename(current_dir)
    if folder_name.startswith(".") or folder_name.lower() in ["venv", ".github","notebooks"]:
        continue
    all_folders.append((folder_name, os.path.relpath(current_dir, root_dir)))

# Collect only top-level folders under root_dir
top_level_folders = [
    d for d in os.listdir(root_dir)
    if os.path.isdir(os.path.join(root_dir, d))
    and not d.startswith(".")
    and d.lower() not in ["venv", ".github", "notebooks", "src"]
]

print(top_level_folders)


# ---- Top-level List of Topics ----
toc.append("## Outline of Sections ")
for folder_name in sorted(top_level_folders):
    toc.append(f"- {to_title_case(folder_name)}")

# ---- Detailed Sections ----
for folder_name, rel_path in sorted(all_folders):
    folder_path = os.path.join(root_dir, rel_path)

    toc.append(f"\n## {to_title_case(folder_name)}\n")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()

    for i, file in enumerate(files, start=1):
        name_raw = os.path.splitext(file)[0]
        name_clean = prefix_pattern.sub("", name_raw).replace("_", " ").replace("-", " ")
        name_title = to_title_case(name_clean)
        file_path = os.path.join(rel_path, file)
        toc.append(f"{i}. [{name_title}]({file_path})")

# Write back into README
new_toc = "\n".join(toc)

with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- TOC START -->)(.*?)(<!-- TOC END -->)"
updated_content = re.sub(pattern, f"\\1\n{new_toc}\n\\3", readme_content, flags=re.DOTALL)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"✅ Updated {readme_path} with List of Topics + sections")
