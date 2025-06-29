import subprocess
from pathlib import Path

commands = [
    ['git', 'checkout', '-b', 'agent_1'],
]
for cmd in commands:
    subprocess.run(cmd, check=False)

Path('description.MD').write_text('simple experimentation with OpenAI-agents-python repo\n')
subprocess.run(['git', 'add', 'description.MD'], check=False)
subprocess.run(['git', 'commit', '-m', 'Add description for agent_1'], check=False)
subprocess.run(['git', 'push', '-u', 'origin', 'agent_1'], check=False)
