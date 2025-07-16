import json
import re

# Function to infer domain from tags
def infer_domain(tags):
    domain_tag = tags[1] if len(tags) > 1 else "general"
    domain_map = {
        "Biology": "Biology",
        "Physics": "Physics",
        "Chemistry": "Chemistry",
        "Material": "Materials Science"
    }
    return domain_map.get(domain_tag, "Science General")

# Function to infer task_type from tags and query
def infer_task_type(tags, query):
    specific_tag = tags[3] if len(tags) > 3 else "general"
    query_lower = query.lower()
    task_type_map = {
        "protein_description_generation": "Protein Biochemistry",
        "physics_literature_QA": "Astrophysics" if "dark matter" in query_lower else "Electromagnetism" if "coils" in query_lower else "Physics General",
        "literature_multi_choice_question": "Medicinal Chemistry",
        "material_literature_QA": "Condensed Matter Physics",
        "high_school_physics_calculation": "Mechanics"
    }
    return task_type_map.get(specific_tag, "Science General")

# Function to infer difficulty from tags
def infer_difficulty(tags):
    level_tag = tags[2] if len(tags) > 2 else "general"
    difficulty_map = {
        "L1": "medium",
        "L3": "hard",
        "L5": "expert"
    }
    return difficulty_map.get(level_tag, "medium")

# Function to extract answer text from query based on gt
def extract_answer_text(query, gt, specific_tag):
    if specific_tag == "protein_description_generation":
        return gt  # Return full text for protein description
    # Extract the letter from gt (e.g., "A") and escape it for regex
    letter = re.escape(gt.strip())
    # Find the answer text in the query
    try:
        match = re.search(rf"{letter}\.\s*([^\n]+)", query)
        if match:
            return f"{gt}. {match.group(1).strip()}"
    except re.PatternError:
        # Fallback if regex fails due to malformed pattern
        return gt
    return gt  # Fallback to gt if answer text not found

# Function to determine evaluation metric
def determine_evaluation_metric(specific_tag):
    if specific_tag == "protein_description_generation":
        return "semantic_similarity"  # Detailed text requires meaning-based evaluation
    return "exact_match"  # Multiple-choice requires precise matching

# Load input JSON file
input_file = "../convert-json/SciKnowEval.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=22):  # Start from SCI_022 to continue from SciEval
    specific_tag = item["tag"][3] if len(item["tag"]) > 3 else "general"
    task_id = f"SCI_{i:03d}"  # e.g., SCI_022, SCI_023, ...
    answer = extract_answer_text(item["query"], item["gt"], specific_tag)
    output_item = {
        "task_id": task_id,
        "domain": infer_domain(item["tag"]),
        "task_type": infer_task_type(item["tag"], item["query"]),
        "prompt": item["query"],
        "expected_answer": answer,
        "difficulty": infer_difficulty(item["tag"]),
        "evaluation_metric": determine_evaluation_metric(specific_tag)
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "converted_sciknoweval_data.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")