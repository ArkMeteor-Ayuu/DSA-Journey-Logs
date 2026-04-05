#!/usr/bin/env python3
"""
Interactive tracker for DSA logs.

What this script does:
1) Updates the main README folder structure + progress counts.
2) Lets you add/update a detailed solve log via terminal prompts.
3) Generates a calendar-style README log for review.

Usage:
    python tracker.py
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
README_PATH = ROOT / "README.md"
README_LOG_PATH = ROOT / "Log.md"
LOG_DATA_PATH = ROOT / "solve_logs.json"
IST_TIMEZONE = ZoneInfo("Asia/Kolkata")

PROBLEM_FILE_EXTENSIONS = {".py"}
PLATFORM_FOLDERS = {"leatcode", "neetcode", "leetcode"}
IGNORED_ROOT_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".vscode",
}

TOPIC_FOLDER_ALIASES = {
    "arrays": ["array & hashing", "arrays"],
    "strings": ["strings", "string"],
    "linked list": ["linked list", "linked-list"],
    "trees": ["trees", "tree"],
    "graphs": ["graphs", "graph"],
    "dynamic programming": ["dynamic programming", "dp"],
}

# User-facing fields for detailed solve logs.
LOG_FIELDS = [
    "Question Name",
    "Platform",
    "Link",
    "Topic",
    "Sub-topic",
    "Date",
    "Day",
    "Time Taken",
    "Attempt Count",
    "Problem Type",
    "Constraint",
    "Technique Used",
    "Pattern Recognition",
    "Approach Summary",
    "Analysis of LeetCode/NeetCode",
    "Tags",
    "Time Complexity",
    "Space Complexity",
    "Better Approach?",
    "Optimization Idea",
    "Key Insight You Missed",
]

REQUIRED_METADATA_KEYS = {
    "problem",
    "platform",
    "link",
    "topic",
    "sub-topic",
    "time taken",
    "attempts",
    "problem type",
    "constraint",
    "technique used",
    "pattern recognition",
    "approach summary",
    "analysis of leetcode/neetcode",
    "tags",
    "time complexity",
    "space complexity",
}


def now_ist() -> datetime:
    """Return current datetime in IST."""
    return datetime.now(IST_TIMEZONE)


def normalize_name(value: str) -> str:
    """Normalize topic/folder names for loose matching."""
    value = value.lower().strip()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def sanitize_cell(value: str) -> str:
    """Keep markdown table cells valid."""
    return value.replace("|", "\\|").strip()


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
            if file_path.is_file() and file_path.suffix.lower() in PROBLEM_FILE_EXTENSIONS
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
    """Update the markdown table under '## 📊 Progress Tracker'."""
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

    updated_lines = lines[: table_start + 2] + new_rows + lines[table_end + 1 :]

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


def iter_problem_files(root: Path) -> list[Path]:
    """Collect all solvable problem files under platform folders."""
    results: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in PROBLEM_FILE_EXTENSIONS:
            continue
        platform = normalize_name(path.parent.name)
        if platform not in PLATFORM_FOLDERS:
            continue
        results.append(path)

    return sorted(results, key=lambda p: str(p.relative_to(root)).lower())


def parse_problem_metadata(file_path: Path) -> dict[str, str]:
    """Parse top comment metadata block from a problem file."""
    metadata: dict[str, str] = {}
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("#"):
            if line:
                break
            continue

        line = line.lstrip("#").strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    return metadata


def meta_value(metadata: dict[str, str], aliases: list[str], fallback: str = "") -> str:
    """Get first matching value for multiple key aliases."""
    lowered = {k.lower(): v for k, v in metadata.items()}
    for alias in aliases:
        if alias.lower() in lowered and lowered[alias.lower()]:
            return lowered[alias.lower()]
    return fallback


def infer_topic_from_path(file_path: Path) -> str:
    """Use root folder as topic fallback."""
    rel = file_path.relative_to(ROOT).parts
    return rel[0] if rel else ""


def infer_subtopic_from_path(file_path: Path) -> str:
    """Use level folder as sub-topic fallback."""
    rel = file_path.relative_to(ROOT).parts
    return rel[1] if len(rel) > 1 else ""


def choose_problem_file(problem_files: list[Path]) -> Path:
    """Prompt user to choose a problem file by number."""
    print("\nChoose a problem file to log:")
    for idx, path in enumerate(problem_files, start=1):
        print(f"  {idx}. {path.relative_to(ROOT)}")

    while True:
        raw = input("Enter number (or direct relative path): ").strip()
        if not raw:
            continue

        if raw.isdigit():
            number = int(raw)
            if 1 <= number <= len(problem_files):
                return problem_files[number - 1]
            print("Invalid number. Try again.")
            continue

        candidate = (ROOT / raw).resolve()
        if candidate.exists() and candidate.is_file():
            return candidate

        print("Path not found. Try again.")


def load_logs(log_path: Path) -> list[dict[str, str]]:
    """Load existing logs if file exists."""
    if not log_path.exists():
        return []

    data = json.loads(log_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        cleaned: list[dict[str, str]] = []
        for row in data:
            if isinstance(row, dict):
                cleaned.append({str(k): str(v) for k, v in row.items()})
        return cleaned
    return []


def find_existing_log(logs: list[dict[str, str]], file_path: Path) -> dict[str, str] | None:
    """Find latest entry by exact file path key."""
    rel = str(file_path.relative_to(ROOT))
    for row in reversed(logs):
        if row.get("File") == rel:
            return row
    return None


def prompt_text(field: str, default: str = "") -> str:
    """Prompt with optional default."""
    suffix = f" [{default}]" if default else ""
    value = input(f"{field}{suffix}: ").strip()
    if value:
        return value
    return default


def ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    """Prompt for y/n input with default."""
    suffix = "[Y/n]" if default_yes else "[y/N]"
    raw = input(f"{prompt} {suffix}: ").strip().lower()
    if not raw:
        return default_yes
    return raw in {"y", "yes"}


def metadata_is_complete(metadata: dict[str, str]) -> bool:
    """Check whether file metadata has all required keys."""
    lowered = {key.lower() for key in metadata}
    return REQUIRED_METADATA_KEYS.issubset(lowered)


def get_pending_problem_files(root: Path) -> list[Path]:
    """Get modified/untracked problem files from git working tree."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return []

    if result.returncode != 0:
        return []

    pending: list[Path] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        rel_path = line[3:].strip()
        if " -> " in rel_path:
            rel_path = rel_path.split(" -> ", 1)[1].strip()

        # git status --porcelain can quote paths with spaces.
        if rel_path.startswith('"') and rel_path.endswith('"') and len(rel_path) >= 2:
            rel_path = rel_path[1:-1]

        candidate = (root / rel_path).resolve()
        if not candidate.exists() or not candidate.is_file():
            continue
        if candidate.suffix.lower() not in PROBLEM_FILE_EXTENSIONS:
            continue
        if normalize_name(candidate.parent.name) not in PLATFORM_FOLDERS:
            continue
        pending.append(candidate)

    return sorted(set(pending), key=lambda p: str(p.relative_to(root)).lower())


def collect_log_details(file_path: Path, existing: dict[str, str] | None) -> dict[str, str]:
    """Build one complete log row from metadata + user prompts."""
    defaults = build_default_log_values(file_path, existing)

    print("\nEnter solve details (press Enter to keep default shown in brackets).")
    row: dict[str, str] = {}
    for field in LOG_FIELDS:
        row[field] = prompt_text(field, defaults.get(field, ""))

    row["File"] = str(file_path.relative_to(ROOT))
    row["Logged At"] = now_ist().strftime("%Y-%m-%d %H:%M:%S IST")
    return row


def build_default_log_values(file_path: Path, existing: dict[str, str] | None) -> dict[str, str]:
    """Build default log values from metadata and fallback rules."""
    metadata = parse_problem_metadata(file_path)
    now = now_ist()

    defaults = {
        "Question Name": meta_value(metadata, ["Problem", "Question Name"], file_path.stem),
        "Platform": meta_value(metadata, ["Platform"], file_path.parent.name),
        "Link": meta_value(metadata, ["Link"]),
        "Topic": meta_value(metadata, ["Topic"], infer_topic_from_path(file_path)),
        "Sub-topic": meta_value(metadata, ["Sub-topic"], infer_subtopic_from_path(file_path)),
        "Date": now.strftime("%Y-%m-%d"),
        "Day": now.strftime("%A"),
        "Time Taken": meta_value(metadata, ["Time Taken", "Time Taken + Attempts"]),
        "Attempt Count": meta_value(metadata, ["Attempt Count", "Attempts"]),
        "Problem Type": meta_value(metadata, ["Problem Type"]),
        "Constraint": meta_value(metadata, ["Constraint", "Constraints"]),
        "Technique Used": meta_value(metadata, ["Technique Used"]),
        "Pattern Recognition": meta_value(metadata, ["Pattern Recognition"]),
        "Approach Summary": meta_value(metadata, ["Approach Summary"]),
        "Analysis of LeetCode/NeetCode": meta_value(
            metadata,
            ["Analysis of LeetCode/NeetCode", "Analysis"],
        ),
        "Tags": meta_value(metadata, ["Tags"]),
        "Time Complexity": meta_value(metadata, ["Time Complexity"]),
        "Space Complexity": meta_value(metadata, ["Space Complexity"]),
        "Better Approach?": meta_value(metadata, ["Better Approach?"]),
        "Optimization Idea": meta_value(metadata, ["Optimization Idea"]),
        "Key Insight You Missed": meta_value(metadata, ["Key Insight You Missed"]),
    }

    if existing:
        for key in defaults:
            if not defaults[key]:
                defaults[key] = existing.get(key, "")

    return defaults


def collect_log_details_auto(file_path: Path, existing: dict[str, str] | None) -> dict[str, str]:
    """Build one complete log row without prompting (metadata-first mode)."""
    defaults = build_default_log_values(file_path, existing)
    row = {field: defaults.get(field, "") for field in LOG_FIELDS}
    row["File"] = str(file_path.relative_to(ROOT))
    row["Logged At"] = now_ist().strftime("%Y-%m-%d %H:%M:%S IST")
    return row


def add_edit_markers(logs: list[dict[str, str]], row: dict[str, str]) -> dict[str, str]:
    """Attach edit markers and prior edit date details for the same file."""
    file_key = row.get("File", "")
    same_file = [item for item in logs if item.get("File") == file_key]

    if not same_file:
        row["Edited"] = "No"
        row["Previous Logged Date"] = ""
        row["Previous Logged At"] = ""
        row["Last Edited At"] = row.get("Logged At", "")
        return row

    latest = same_file[-1]
    row["Edited"] = "Yes"
    row["Previous Logged Date"] = latest.get("Date", "")
    row["Previous Logged At"] = latest.get("Logged At", "")
    row["Last Edited At"] = row.get("Logged At", "")
    return row


def upsert_log(logs: list[dict[str, str]], row: dict[str, str]) -> list[dict[str, str]]:
    """Replace existing latest row for the same file and date, else append."""
    new_logs = list(logs)
    file_key = row.get("File", "")
    date_key = row.get("Date", "")

    replaced = False
    for i in range(len(new_logs) - 1, -1, -1):
        item = new_logs[i]
        if item.get("File") == file_key and item.get("Date") == date_key:
            new_logs[i] = row
            replaced = True
            break

    if not replaced:
        new_logs.append(row)

    return new_logs


def save_logs(log_path: Path, logs: list[dict[str, str]]) -> None:
    """Persist log rows to JSON."""
    log_path.write_text(json.dumps(logs, indent=2), encoding="utf-8")


def format_calendar_log(logs: list[dict[str, str]]) -> str:
    """Build markdown for the detailed calendar-style solve log."""
    lines = [
        "# Solve Calendar Log",
        "",
        "Auto-generated by tracker.py.",
        "",
        "This log is organized by date and includes problem metadata, analysis, and review notes.",
        "",
    ]

    if not logs:
        lines.append("No solve logs yet. Run `python tracker.py` and add your first entry.")
        lines.append("")
        return "\n".join(lines)

    def sort_key(item: dict[str, str]) -> tuple[str, str]:
        return (item.get("Date", ""), item.get("Logged At", ""))

    ordered = sorted(logs, key=sort_key, reverse=True)
    current_date = ""

    for item in ordered:
        date = item.get("Date", "Unknown Date")
        day = item.get("Day", "")
        if date != current_date:
            lines.append(f"## {sanitize_cell(date)} ({sanitize_cell(day)})")
            lines.append("")
            current_date = date

        lines.append(f"### {sanitize_cell(item.get('Question Name', 'Unknown Question'))}")
        lines.append("")
        lines.append(f"- Platform: {sanitize_cell(item.get('Platform', ''))}")
        lines.append(f"- Link: {sanitize_cell(item.get('Link', ''))}")
        lines.append(f"- Topic: {sanitize_cell(item.get('Topic', ''))}")
        lines.append(f"- Sub-topic: {sanitize_cell(item.get('Sub-topic', ''))}")
        lines.append(f"- Time Taken: {sanitize_cell(item.get('Time Taken', ''))}")
        lines.append(f"- Attempt Count: {sanitize_cell(item.get('Attempt Count', ''))}")
        lines.append(f"- Problem Type: {sanitize_cell(item.get('Problem Type', ''))}")
        lines.append(f"- Constraint: {sanitize_cell(item.get('Constraint', ''))}")
        lines.append(f"- Technique Used: {sanitize_cell(item.get('Technique Used', ''))}")
        lines.append(f"- Pattern Recognition: {sanitize_cell(item.get('Pattern Recognition', ''))}")
        lines.append(f"- Approach Summary: {sanitize_cell(item.get('Approach Summary', ''))}")
        lines.append(
            "- Analysis of LeetCode/NeetCode: "
            f"{sanitize_cell(item.get('Analysis of LeetCode/NeetCode', ''))}"
        )
        lines.append(f"- Tags: {sanitize_cell(item.get('Tags', ''))}")
        lines.append(f"- Time Complexity: {sanitize_cell(item.get('Time Complexity', ''))}")
        lines.append(f"- Space Complexity: {sanitize_cell(item.get('Space Complexity', ''))}")
        lines.append(f"- Better Approach?: {sanitize_cell(item.get('Better Approach?', ''))}")
        lines.append(f"- Optimization Idea: {sanitize_cell(item.get('Optimization Idea', ''))}")
        lines.append(
            f"- Key Insight You Missed: {sanitize_cell(item.get('Key Insight You Missed', ''))}"
        )
        lines.append(f"- File: {sanitize_cell(item.get('File', ''))}")
        lines.append(f"- Edited: {sanitize_cell(item.get('Edited', 'No'))}")
        if item.get("Previous Logged Date"):
            lines.append(
                f"- Previous Logged Date: {sanitize_cell(item.get('Previous Logged Date', ''))}"
            )
        if item.get("Previous Logged At"):
            lines.append(f"- Previous Logged At: {sanitize_cell(item.get('Previous Logged At', ''))}")
        if item.get("Last Edited At"):
            lines.append(f"- Last Edited At: {sanitize_cell(item.get('Last Edited At', ''))}")
        lines.append(f"- Logged At: {sanitize_cell(item.get('Logged At', ''))}")
        lines.append("")

    return "\n".join(lines)


def update_calendar_readme(readme_log_path: Path, logs: list[dict[str, str]]) -> None:
    """Write calendar log markdown file."""
    readme_log_path.write_text(format_calendar_log(logs), encoding="utf-8")


def is_problem_file(path: Path) -> bool:
    """Return True when a path looks like a tracked platform problem file."""
    if not path.is_file():
        return False
    if path.suffix.lower() not in PROBLEM_FILE_EXTENSIONS:
        return False
    return normalize_name(path.parent.name) in PLATFORM_FOLDERS


def build_commit_message_from_staged_files(staged_rel_paths: list[str]) -> str:
    """Build commit message from staged problem file names."""
    names: list[str] = []

    for rel in staged_rel_paths:
        candidate = (ROOT / rel).resolve()
        if candidate.exists() and is_problem_file(candidate):
            metadata = parse_problem_metadata(candidate)
            problem_name = meta_value(metadata, ["Problem", "Question Name"], candidate.stem)
            if problem_name and problem_name not in names:
                names.append(problem_name)

    if names:
        return f"Adding file for solved problem {', '.join(names)}"

    return "Update repository files"


def git_commit_and_push() -> None:
    """Commit and push changes to GitHub."""
    try:
        # Stage all repository changes.
        subprocess.run(
            ["git", "add", "-A"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )

        staged_result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        staged_rel_paths = [line.strip() for line in staged_result.stdout.splitlines() if line.strip()]

        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=ROOT,
            capture_output=True,
        )

        if result.returncode != 0:  # Changes exist
            commit_message = build_commit_message_from_staged_files(staged_rel_paths)

            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )

            # Push to GitHub
            push_result = subprocess.run(
                ["git", "push"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            if push_result.returncode == 0:
                print("Changes pushed to GitHub successfully.")
            else:
                print("Git push encountered an issue. Check your connection.")
        else:
            print("No changes to commit.")

    except Exception as e:
        print(f"Git operations skipped: {e}")


def log_one_file(logs: list[dict[str, str]], file_path: Path) -> list[dict[str, str]]:
    """Collect details for one file and write log storage."""
    metadata = parse_problem_metadata(file_path)
    existing = find_existing_log(logs, file_path)

    if not metadata_is_complete(metadata):
        print(f"Metadata format is incomplete for: {file_path.relative_to(ROOT)}")
        print("Tracker will ask for all required details now.")
        row = collect_log_details(file_path, existing)
    else:
        row = collect_log_details_auto(file_path, existing)
        print(f"Metadata is complete. Auto-logging: {file_path.relative_to(ROOT)}")

    row = add_edit_markers(logs, row)
    logs = upsert_log(logs, row)
    save_logs(LOG_DATA_PATH, logs)
    print(f"Saved solve log for: {file_path.relative_to(ROOT)}")
    return logs


def main() -> None:
    update_readme(README_PATH, ROOT)
    print("README Progress Tracker updated successfully.")
    print("Using timezone: Asia/Kolkata (IST).")

    problem_files = iter_problem_files(ROOT)
    if not problem_files:
        print("No problem files found. Exiting.")
        return

    logs = load_logs(LOG_DATA_PATH)
    processed: set[Path] = set()

    pending_files = get_pending_problem_files(ROOT)
    if pending_files:
        print("Found modified/untracked problem files. Processing one by one.")
        for file_path in pending_files:
            print(f"\nCandidate file: {file_path.relative_to(ROOT)}")
            logs = log_one_file(logs, file_path)
            processed.add(file_path)
    else:
        print("No modified/untracked problem files found.")

    while ask_yes_no("Do you want to update another file?", default_yes=False):
        latest_pending = [p for p in get_pending_problem_files(ROOT) if p not in processed]

        if latest_pending:
            print("Found modified/untracked files not yet logged in this run.")
            chosen = choose_problem_file(latest_pending)
            logs = log_one_file(logs, chosen)
            processed.add(chosen)
            continue

        print("No modified/untracked files pending.")
        if not ask_yes_no("Do you want to update an unedited file?", default_yes=False):
            break

        chosen = choose_problem_file(problem_files)
        logs = log_one_file(logs, chosen)
        processed.add(chosen)

    update_calendar_readme(README_LOG_PATH, logs)
    print("Log.md generated successfully.")

    # Commit and push to GitHub
    git_commit_and_push()


if __name__ == "__main__":
    main()
