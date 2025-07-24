#!/usr/bin/env python3
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List
import pytz
from datetime import datetime

# ---------- Logging ----------
IST = pytz.timezone("Asia/Kolkata")

class ISTFormatter(logging.Formatter):
    def converter(self, timestamp):
        return datetime.fromtimestamp(timestamp, IST).timetuple()

formatter = ISTFormatter("%(asctime)s [%(levelname)s] %(message)s")

# ---------- CLI ----------
parser = argparse.ArgumentParser(description="Aggregate evaluated LLM benchmark results across iterations for a single model")
parser.add_argument("--domain", type=str, required=True, help="Domain name (e.g., Mathematics)")
parser.add_argument("--test-file", type=str, required=True, help="Test file name without extension (e.g., test_algebra)")
parser.add_argument("--iterations", type=int, required=True, help="Number of iterations to aggregate")
parser.add_argument("--model", type=str, required=True, help="Model name (e.g., qwen2.5:1.5b)")
cli_args = parser.parse_args()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f"logs/Domain/{cli_args.domain}/aggregate_results.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
for h in logging.getLogger().handlers:
    h.setFormatter(formatter)
logger = logging.getLogger(__name__)

# ---------- Aggregation ----------
def aggregate_metrics(model_name: str, all_results: List[List[Dict]]) -> Dict:
    total_iterations = len(all_results)
    aggregated = {
        "model_name": model_name,
        "domain": cli_args.domain,
        "test_file": cli_args.test_file,
        "total_iterations": total_iterations,
        "metrics": {}
    }
    
    # Combine results from all iterations for the model
    combined_results = []
    for iteration_results in all_results:
        combined_results.extend(iteration_results)
    
    total_tasks = len(combined_results)
    successful_tasks = [r for r in combined_results if r["success"]]
    correct_tasks = sum(r["correct"] for r in successful_tasks)
    
    # Calculate averages
    aggregated["metrics"]["accuracy_percent"] = (correct_tasks / total_tasks * 100) if total_tasks else 0.0
    aggregated["metrics"]["avg_latency_ms"] = (
        sum(r["latency_ms"] for r in successful_tasks) / len(successful_tasks)
    ) if successful_tasks else 0.0
    aggregated["metrics"]["avg_memory_peak_mb"] = (
        sum(r["memory_peak_mb"] for r in successful_tasks) / len(successful_tasks)
    ) if successful_tasks else 0.0
    aggregated["metrics"]["avg_throughput_tps"] = (
        sum(r["throughput_tps"] for r in successful_tasks) / len(successful_tasks)
    ) if successful_tasks else 0.0
    aggregated["metrics"]["total_tokens"] = sum(r["total_tokens"] for r in successful_tasks)
    aggregated["metrics"]["avg_ref_throughput_tps"] = (
        sum(r["ref_throughput_tps"] for r in successful_tasks) / len(successful_tasks)
    ) if successful_tasks else 0.0
    aggregated["metrics"]["total_ref_tokens"] = sum(r["ref_total_tokens"] for r in successful_tasks)
    aggregated["metrics"]["total_tasks"] = total_tasks
    aggregated["metrics"]["successful_tasks"] = len(successful_tasks)
    aggregated["metrics"]["correct_tasks"] = correct_tasks
    
    return aggregated

def save_aggregated_results(model_name: str, aggregated: Dict, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)
    logger.info("Saved aggregated results for %s to %s", model_name, path)

# ---------- Main ----------
def main():
    # Create necessary directories
    Path(f"Final_Results/{cli_args.domain}").mkdir(parents=True, exist_ok=True)
    Path(f"logs/Domain/{cli_args.domain}").mkdir(parents=True, exist_ok=True)

    model_name = cli_args.model
    model_name_safe = model_name.replace(':', '_').replace('b', 'B')
    all_results = []
    
    # Load evaluated results for each iteration
    for iteration in range(1, cli_args.iterations + 1):
        result_path = f"Final_Results/{cli_args.domain}/evaluated/{model_name_safe}/{cli_args.test_file}_results_iter_{iteration}.json"
        if not Path(result_path).is_file():
            logger.error("Result file not found: %s", result_path)
            continue
        try:
            with open(result_path, encoding="utf-8") as f:
                results = json.load(f)
            all_results.append(results)
            logger.info("Loaded evaluated results for %s, iteration %d", model_name, iteration)
        except Exception as e:
            logger.error("Failed to load %s: %s", result_path, e)
            continue
    
    if not all_results:
        logger.error("No valid results found for %s", model_name)
        sys.exit(1)
    
    # Aggregate metrics
    aggregated = aggregate_metrics(model_name, all_results)
    
    # Save aggregated results
    output_path = f"Final_Results/{cli_args.domain}/{model_name_safe}/aggregated_results_{cli_args.test_file}.json"
    save_aggregated_results(model_name, aggregated, output_path)

if __name__ == "__main__":
    main()