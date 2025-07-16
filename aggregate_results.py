import json
import os
from statistics import mean, stdev

results_dir = "Resultszz/Mathematics"
models = ["qwen2.5_1.5B", "llama3.2_1B"]

# Initialize data structure to store results for each model
all_iterations = {model: [] for model in models}

# Process results for each model
for model in models:
    for file in os.listdir(results_dir):
        if file.startswith(f"{model}_test_wp_results_iter_") and file.endswith(".json"):
            try:
                with open(os.path.join(results_dir, file), 'r') as f:
                    data = json.load(f)
                    total = len(data)
                    correct = sum(r["correct"] for r in data)
                    math_correct = sum(r["correct"] for r in data if r["task_id"].startswith("MATH"))
                    fact_correct = sum(r["correct"] for r in data if r["task_id"].startswith("FACT"))
                    math_count = sum(1 for r in data if r["task_id"].startswith("MATH"))
                    fact_count = sum(1 for r in data if r["task_id"].startswith("FACT"))
                    avg_latency = sum(r["latency_ms"] for r in data if r["success"]) / total if total > 0 else 0
                    avg_memory = sum(r["memory_mb"] for r in data if r["success"]) / total if total > 0 else 0
                    avg_cpu_time = sum(r["cpu_time_s"] for r in data if r["success"]) * 1000 / total if total > 0 else 0
                    avg_total_duration_ms = sum(r["total_duration_ns"] / 1e6 for r in data if r["success"]) / total if total > 0 else 0
                    avg_load_duration_ms = sum(r["load_duration_ns"] / 1e6 for r in data if r["success"]) / total if total > 0 else 0
                    avg_prompt_eval_count = sum(r["prompt_eval_count"] for r in data if r["success"]) / total if total > 0 else 0
                    avg_prompt_eval_duration_ms = sum(r["prompt_eval_duration_ns"] / 1e6 for r in data if r["success"]) / total if total > 0 else 0
                    avg_eval_count = sum(r["eval_count"] for r in data if r["success"]) / total if total > 0 else 0
                    avg_eval_duration_ms = sum(r["eval_duration_ns"] / 1e6 for r in data if r["success"]) / total if total > 0 else 0
                    all_iterations[model].append({
                        "file": file,
                        "total": total,
                        "correct": correct,
                        "accuracy": correct / total * 100 if total > 0 else 0,
                        "math_accuracy": math_correct / math_count * 100 if math_count > 0 else 0,
                        "fact_accuracy": fact_correct / fact_count * 100 if fact_count > 0 else 0,
                        "avg_latency_ms": avg_latency,
                        "avg_memory_mb": avg_memory,
                        "avg_cpu_time_ms": avg_cpu_time,
                        "avg_total_duration_ms": avg_total_duration_ms,
                        "avg_load_duration_ms": avg_load_duration_ms,
                        "avg_prompt_eval_count": avg_prompt_eval_count,
                        "avg_prompt_eval_duration_ms": avg_prompt_eval_duration_ms,
                        "avg_eval_count": avg_eval_count,
                        "avg_eval_duration_ms": avg_eval_duration_ms
                    })
            except Exception as e:
                print(f"Error processing {file} for model {model}: {str(e)}")

# Aggregate and save results for each model
for model in models:
    iterations = all_iterations[model]
    output_file = os.path.join(results_dir, f"aggregation_summary_{model}_test_wp.json")
    if iterations:
        avg_accuracy = mean(r["accuracy"] for r in iterations)
        avg_math_accuracy = mean(r["math_accuracy"] for r in iterations)
        avg_fact_accuracy = mean(r["fact_accuracy"] for r in iterations)
        std_accuracy = stdev([r["accuracy"] for r in iterations]) if len(iterations) > 1 else 0
        std_math_accuracy = stdev([r["math_accuracy"] for r in iterations]) if len(iterations) > 1 else 0
        std_fact_accuracy = stdev([r["fact_accuracy"] for r in iterations]) if len(iterations) > 1 else 0
        avg_latency = mean(r["avg_latency_ms"] for r in iterations)
        avg_memory = mean(r["avg_memory_mb"] for r in iterations)
        avg_cpu_time = mean(r["avg_cpu_time_ms"] for r in iterations)
        avg_total_duration_ms = mean(r["avg_total_duration_ms"] for r in iterations)
        avg_load_duration_ms = mean(r["avg_load_duration_ms"] for r in iterations)
        avg_prompt_eval_count = mean(r["avg_prompt_eval_count"] for r in iterations)
        avg_prompt_eval_duration_ms = mean(r["avg_prompt_eval_duration_ms"] for r in iterations)
        avg_eval_count = mean(r["avg_eval_count"] for r in iterations)
        avg_eval_duration_ms = mean(r["avg_eval_duration_ms"] for r in iterations)
        
        print(f"\nAggregation Summary for {model}:")
        print(f"Total Iterations: {len(iterations)}")
        print(f"Average Accuracy: {avg_accuracy:.2f}% ± {std_accuracy:.2f}%")
        print(f"Average Math Accuracy: {avg_math_accuracy:.2f}% ± {std_math_accuracy:.2f}%")
        print(f"Average Facts Accuracy: {avg_fact_accuracy:.2f}% ± {std_fact_accuracy:.2f}%")
        print(f"Average Latency: {avg_latency:.2f}ms")
        print(f"Average Memory: {avg_memory:.2f}MB")
        print(f"Average CPU Time: {avg_cpu_time:.2f}ms")
        print(f"Average Total Duration: {avg_total_duration_ms:.2f}ms")
        print(f"Average Load Duration: {avg_load_duration_ms:.2f}ms")
        print(f"Average Prompt Eval Count: {avg_prompt_eval_count:.2f} tokens")
        print(f"Average Prompt Eval Duration: {avg_prompt_eval_duration_ms:.2f}ms")
        print(f"Average Eval Count: {avg_eval_count:.2f} tokens")
        print(f"Average Eval Duration: {avg_eval_duration_ms:.2f}ms")
        
        # Save model-specific results
        with open(output_file, "w") as f:
            json.dump({
                "model": model,
                "iterations": iterations,
                "summary": {
                    "total_iterations": len(iterations),
                    "avg_accuracy": avg_accuracy,
                    "std_accuracy": std_accuracy,
                    "avg_math_accuracy": avg_math_accuracy,
                    "std_math_accuracy": std_math_accuracy,
                    "avg_fact_accuracy": avg_fact_accuracy,
                    "std_fact_accuracy": std_fact_accuracy,
                    "avg_latency_ms": avg_latency,
                    "avg_memory_mb": avg_memory,
                    "avg_cpu_time_ms": avg_cpu_time,
                    "avg_total_duration_ms": avg_total_duration_ms,
                    "avg_load_duration_ms": avg_load_duration_ms,
                    "avg_prompt_eval_count": avg_prompt_eval_count,
                    "avg_prompt_eval_duration_ms": avg_prompt_eval_duration_ms,
                    "avg_eval_count": avg_eval_count,
                    "avg_eval_duration_ms": avg_eval_duration_ms
                }
            }, f, indent=2)
        
        print(f"Aggregation summary for {model} saved to {output_file}")
    else:
        print(f"No valid result files found for model {model}")
        with open(output_file, "w") as f:
            json.dump({
                "model": model,
                "error": "No valid result files found"
            }, f, indent=2)
        print(f"Error summary for {model} saved to {output_file}")