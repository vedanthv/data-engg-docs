import os
import re
import yaml

BASE_DIR = "internals-docs-code"
MKDOCS_FILE = "mkdocs.yml"
NAV_GENERATED = "nav_generated.yml"

IGNORE_FOLDERS = {"notebooks", "__pycache__", ".git", ".github"}

def clean_title(filename: str) -> str:
    name = os.path.splitext(filename)[0]
    name = re.sub(r"^\d+[_-]?", "", name)
    return name.replace("_", " ").replace("-", " ").title()

def build_nav_for_folder(folder: str):
    entries = []
    has_subfolders = False
    for item in sorted(os.listdir(folder)):
        path = os.path.join(folder, item)
        rel_path = os.path.relpath(path, BASE_DIR)
        if os.path.isdir(path):
            if item in IGNORE_FOLDERS:
                continue
            entries.append({clean_title(item): build_nav_for_folder(path)})
        elif item.endswith(".md") and item.lower() != "index.md":
            entries.append({clean_title(item): rel_path.replace("\\", "/")})
        elif item.lower() == "index.md":
            entries.insert(0, {"Index": rel_path.replace("\\", "/")})

    # If no subfolders → wrap flat files under "Topics"
    if not has_subfolders and len(entries) > 1:
        index = None
        others = []
        for e in entries:
            if "Index" in e:
                index = e
            else:
                others.append(e)
        wrapped = []
        if index:
            wrapped.append(index)
        wrapped.append({"Topics": others})
        return wrapped

    return entries

def build_full_nav():
    nav = [{"Home": "index.md"}]
    for section in sorted(os.listdir(BASE_DIR)):
        path = os.path.join(BASE_DIR, section)
        if os.path.isdir(path) and section not in IGNORE_FOLDERS:
            nav.append({clean_title(section): build_nav_for_folder(path)})
        elif section.endswith(".md") and section.lower() != "index.md":
            nav.append({clean_title(section): section})
    return nav

# Dumper with clean indentation
class IndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def main():
    nav_data = {"nav": build_full_nav()}
    nav_text = yaml.dump(
        nav_data,
        Dumper=IndentDumper,
        sort_keys=False,
        allow_unicode=True,
        indent=2,
        default_flow_style=False
    )

    # Save to nav_generated.yml for debugging
    with open(NAV_GENERATED, "w", encoding="utf-8") as f:
        f.write(nav_text)

    # Replace inside mkdocs.yml only between markers
    with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if "# BEGIN AUTO NAV" not in content or "# END AUTO NAV" not in content:
        raise RuntimeError("Please add '# BEGIN AUTO NAV' and '# END AUTO NAV' around nav in mkdocs.yml")

    new_content = re.sub(
        r"(# BEGIN AUTO NAV)(.*?)(# END AUTO NAV)",
        f"\\1\n{nav_text.strip()}\n\\3",
        content,
        flags=re.DOTALL
    )

    with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Updated {MKDOCS_FILE} with generated nav (from {NAV_GENERATED})")

if __name__ == "__main__":
    main()
