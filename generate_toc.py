import os
import re

# Path to your docs folder where README.md lives
root_dir = "internal-docs-code"

toc = ["# Consolidated Table of Contents\n"]

# Scan subfolders inside internal-docs-code
for subdir in sorted(next(os.walk(root_dir))[1]):
    if subdir.startswith(".") or subdir.lower() in ["venv", ".github"]:
        continue

    folder_path = os.path.join(root_dir, subdir)
    md_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]

    if not md_files:
        continue

    toc.append(f"\n## {subdir.capitalize()}\n")
    for md_file in sorted(md_files):
        file_path = os.path.join(subdir, md_file)
        name = os.path.splitext(md_file)[0].replace("_", " ").capitalize()
        toc.append(f"- [{name}]({file_path})")

new_toc = "\n".join(toc)

# Replace section in README.md between <!-- TOC START --> and <!-- TOC END -->
readme_path = os.path.join(root_dir, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- TOC START -->)(.*?)(<!-- TOC END -->)"
updated_content = re.sub(pattern, f"\\1\n{new_toc}\n\\3", readme_content, flags=re.DOTALL)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("✅ Updated internal-docs-code/README.md with consolidated TOC")
