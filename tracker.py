#!/usr/bin/env python3
"""
Update README Progress Tracker based on solved problem files.

Usage:
    python update_progress_tracker.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README_PATH = ROOT / "README.md"

# File extensions considered as solved problem files.
PROBLEM_FILE_EXTENSIONS = {".py"}

# Platform folders that may exist under each level folder.
PLATFORM_FOLDERS = {"leatcode", "neetcode", "leetcode"}

# Folders to ignore at repository root.
IGNORED_ROOT_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".vscode",
}

# Map README topic names to likely folder names.
TOPIC_FOLDER_ALIASES = {
    "arrays": ["array & hashing", "arrays"],
    "strings": ["strings", "string"],
    "linked list": ["linked list", "linked-list"],
    "trees": ["trees", "tree"],
    "graphs": ["graphs", "graph"],
    "dynamic programming": ["dynamic programming", "dp"],
}


def normalize_name(value: str) -> str:
    """Normalize topic/folder names for loose matching."""
    value = value.lower().strip()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def count_problem_files(topic_dir: Path) -> int:
    """Count solved files inside platform folders under a topic directory."""
    total = 0

    for path in topic_dir.rglob("*"):
        if not path.is_dir():
            continue
        if normalize_name(path.name) not in PLATFORM_FOLDERS:
            continue

        total += sum(
            1
            for file_path in path.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() in PROBLEM_FILE_EXTENSIONS
        )

    return total


def build_folder_tree_lines(directory: Path, indent_level: int = 0) -> list[str]:
    """Build a markdown bullet tree containing folders only."""
    lines: list[str] = []

    for entry in sorted(directory.iterdir(), key=lambda path: path.name.lower()):
        if not entry.is_dir():
            continue
        if entry.name in IGNORED_ROOT_DIRS or entry.name.startswith("."):
            continue

        indent = "  " * indent_level
        lines.append(f"{indent}- {entry.name}/")
        lines.extend(build_folder_tree_lines(entry, indent_level + 1))

    return lines


def get_root_folders(root: Path) -> dict[str, Path]:
    """Get normalized root folder names mapped to paths."""
    folders: dict[str, Path] = {}

    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if entry.name in IGNORED_ROOT_DIRS or entry.name.startswith("."):
            continue
        folders[normalize_name(entry.name)] = entry

    return folders


def resolve_topic_count(topic: str, folders: dict[str, Path]) -> int:
    """Resolve solved count for a README topic based on matching root folder names."""
    topic_key = normalize_name(topic)
    candidates = [topic_key]

    if topic_key in TOPIC_FOLDER_ALIASES:
        candidates.extend(TOPIC_FOLDER_ALIASES[topic_key])

    normalized_candidates = [normalize_name(name) for name in candidates]

    for candidate in normalized_candidates:
        if candidate in folders:
            return count_problem_files(folders[candidate])

    return 0


def update_progress_table(content: str, root: Path) -> str:
    """
    Update the markdown table under '## 📊 Progress Tracker'.
    Keeps topic names/order and replaces only solved counts.
    """
    marker = "## 📊 Progress Tracker"
    if marker not in content:
        raise ValueError("README does not contain '## 📊 Progress Tracker' section.")

    lines = content.splitlines()
    start_idx = next(i for i, line in enumerate(lines) if line.strip() == marker)

    table_start = None
    for i in range(start_idx + 1, len(lines)):
        if lines[i].strip().startswith("| Topic | Problems Solved |"):
            table_start = i
            break

    if table_start is None:
        raise ValueError("Progress Tracker table header not found in README.")

    table_end = table_start
    for i in range(table_start + 1, len(lines)):
        if not lines[i].strip().startswith("|"):
            table_end = i - 1
            break
    else:
        table_end = len(lines) - 1

    folders = get_root_folders(root)
    new_rows: list[str] = []
    total_solved = 0

    for i in range(table_start + 2, table_end + 1):
        row = lines[i].strip()
        if not row or row.startswith("|--"):
            continue

        parts = [p.strip() for p in row.strip("|").split("|")]
        if len(parts) != 2:
            new_rows.append(lines[i])
            continue

        topic = parts[0]
        solved_count = resolve_topic_count(topic, folders)
        total_solved += solved_count
        new_rows.append(f"| {topic} | {solved_count} |")

    updated_lines = (
        lines[: table_start + 2]
        + new_rows
        + lines[table_end + 1 :]
    )

    total_line = f"- **Total Solved:** {total_solved}"
    total_idx = None
    for i, line in enumerate(updated_lines):
        if line.strip().startswith("- **Total Solved:**"):
            total_idx = i
            break

    if total_idx is not None:
        updated_lines[total_idx] = total_line

    legacy_marker = "## Progress Tracker"
    legacy_idx = None
    for i, line in enumerate(updated_lines):
        if i > start_idx and line.strip() == legacy_marker:
            legacy_idx = i
            break

    if legacy_idx is not None:
        updated_lines = updated_lines[:legacy_idx]

    return "\n".join(updated_lines) + "\n"


def update_folder_structure_section(content: str, root: Path) -> str:
    """Insert or refresh the folder structure section in the README."""
    marker = "## 🗂️ Folder Structure"
    lines = content.splitlines()
    tree_lines = build_folder_tree_lines(root)
    section_lines = [marker, ""]

    if tree_lines:
        section_lines.extend(tree_lines)
    else:
        section_lines.append("- (no folders found)")

    section_lines.append("")

    if marker in content:
        start_idx = next(i for i, line in enumerate(lines) if line.strip() == marker)
        end_idx = start_idx + 1

        while end_idx < len(lines):
            next_line = lines[end_idx].strip()
            if next_line.startswith("## ") and end_idx > start_idx:
                break
            end_idx += 1

        updated_lines = lines[:start_idx] + section_lines + lines[end_idx:]
    else:
        insert_before = None
        for index, line in enumerate(lines):
            if line.strip() == "## 📊 Progress Tracker":
                insert_before = index
                break

        if insert_before is None:
            raise ValueError("Progress Tracker section not found in README.")

        updated_lines = lines[:insert_before] + section_lines + lines[insert_before:]

    return "\n".join(updated_lines) + "\n"


def update_readme(readme_path: Path, root: Path) -> None:
    """Update the README Progress Tracker table in-place."""
    if not readme_path.exists():
        raise FileNotFoundError(f"README not found at: {readme_path}")

    content = readme_path.read_text(encoding="utf-8")
    updated = update_folder_structure_section(content, root)
    updated = update_progress_table(updated, root)
    readme_path.write_text(updated, encoding="utf-8")


def push_changes(root: Path) -> None:
    """Stage, commit, and push repository changes to the configured remote."""
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)

    diff_result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=root,
        check=False,
    )

    if diff_result.returncode == 0:
        print("No changes to commit.")
        return

    subprocess.run(
        ["git", "commit", "-m", "Update progress tracker"],
        cwd=root,
        check=True,
    )
    subprocess.run(["git", "push"], cwd=root, check=True)
    print("Changes committed and pushed to GitHub successfully.")


def main() -> None:
    update_readme(README_PATH, ROOT)
    print("README Progress Tracker updated successfully.")
    push_changes(ROOT)


if __name__ == "__main__":
    main()
