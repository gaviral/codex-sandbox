import subprocess
from pathlib import Path

START_MARKER = "<!-- Branch Table Start -->"
END_MARKER = "<!-- Branch Table End -->"

def get_branches():
    result = subprocess.run(['git', 'branch', '--format', '%(refname:short)'], capture_output=True, text=True)
    branches = [b.strip() for b in result.stdout.splitlines() if b.strip()]
    return branches

def get_description(branch):
    # Prefer description.MD but fallback to description.md
    result = subprocess.run(['git', 'show', f'{branch}:description.MD'], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(['git', 'show', f'{branch}:description.md'], capture_output=True, text=True)
    if result.returncode != 0:
        return ''
    data = result.stdout.strip()
    return data.splitlines()[0] if data else ''

def build_table():
    lines = ["| Branch | Description |", "|-------|-------------|"]
    for branch in get_branches():
        desc = get_description(branch)
        lines.append(f"| {branch} | {desc} |")
    return "\n".join(lines)

def update_readme(table):
    path = Path('README.md')
    text = path.read_text() if path.exists() else ''
    if START_MARKER in text and END_MARKER in text:
        pre = text.split(START_MARKER)[0]
        post = text.split(END_MARKER)[1]
        new_text = f"{pre}{START_MARKER}\n{table}\n{END_MARKER}{post}"
    else:
        if not text.endswith('\n'):
            text += '\n'
        new_text = f"{text}\n{START_MARKER}\n{table}\n{END_MARKER}\n"
    path.write_text(new_text)

if __name__ == '__main__':
    table = build_table()
    update_readme(table)
