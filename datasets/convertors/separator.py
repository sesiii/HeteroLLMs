import json
import os

# Read the input JSON file
with open('input.json', 'r') as file:
    data = json.load(file)

# Group tasks by task_type
task_type_groups = {}
for item in data:
    task_type = item['task_type']
    if task_type not in task_type_groups:
        task_type_groups[task_type] = []
    task_type_groups[task_type].append(item)

# Create output directory if it doesn't exist
output_dir = 'task_types'
os.makedirs(output_dir, exist_ok=True)

# Write separate JSON files for each task_type
for task_type, tasks in task_type_groups.items():
    # Replace spaces with underscores and convert to lowercase for filename
    filename = os.path.join(output_dir, f'{task_type.lower().replace(" ", "_")}.json')
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=2)