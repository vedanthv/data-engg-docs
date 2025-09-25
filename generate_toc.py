import os
import re

root_dir = "internals-docs-code"
readme_path = os.path.join(root_dir, "README.md")

toc = ["## 📑 Consolidated Table of Contents\n"]

# Regex to strip numeric prefixes (like 01-, 02-)
prefix_pattern = re.compile(r"^\d+-")

def to_title_case(name: str) -> str:
    """Convert a cleaned filename or folder name into Title Case."""
    return " ".join(word.capitalize() for word in name.split())

# List subdirectories inside root_dir
subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

for subdir in sorted(subdirs):
    if subdir.startswith(".") or subdir.lower() in ["venv", ".github",'notebooks']:
        continue

    folder_path = os.path.join(root_dir, subdir)
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not files:
        continue

    # Section header (folder name → Title Case)
    toc.append(f"\n### {to_title_case(subdir)}\n")

    for i, file in enumerate(sorted(files), start=1):
        # Strip extension + numeric prefix
        name_raw = os.path.splitext(file)[0]  # remove extension
        name_clean = prefix_pattern.sub("", name_raw).replace("_", " ").replace("-", " ")
        name_title = to_title_case(name_clean)

        file_path = os.path.join(subdir, file)
        toc.append(f"{i}. [{name_title}]({file_path})")

new_toc = "\n".join(toc)

# Replace section in README.md between <!-- TOC START --> and <!-- TOC END -->
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- TOC START -->)(.*?)(<!-- TOC END -->)"
updated_content = re.sub(pattern, f"\\1\n{new_toc}\n\\3", readme_content, flags=re.DOTALL)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"✅ Updated {readme_path} with numbered TOC in Title Case (all files included)")
