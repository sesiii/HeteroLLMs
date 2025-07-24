#!/usr/bin/env python3
import tiktoken      
REF_TOKENIZER = tiktoken.get_encoding("gpt2")   
import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from difflib import SequenceMatcher
from multiprocessing import Manager, Pool
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

import psutil
import pytz
import requests
import tenacity
from dotenv import load_dotenv

# ---------- Logging ----------
load_dotenv()
IST = pytz.timezone("Asia/Kolkata")

class ISTFormatter(logging.Formatter):
    def converter(self, timestamp):
        return datetime.fromtimestamp(timestamp, IST).timetuple()

formatter = ISTFormatter("%(asctime)s [%(levelname)s] %(message)s")

# ---------- CLI ----------
parser = argparse.ArgumentParser(description="LLM benchmark – more metrics")
parser.add_argument("--iteration", type=int, default=1, help="iteration number")
parser.add_argument(
    "--model",
    type=str,
    default="all",
    help="Model to run (use 'all' to run all models)",
)
parser.add_argument(
    "--domain",
    type=str,
    required=True,
    help="Domain name (e.g., Mathematics)",
)
parser.add_argument(
    "--test-file",
    type=str,
    required=True,
    help="Test file name without extension (e.g., test_algebra)",
)
cli_args = parser.parse_args()

# Set up logging with domain-specific log file
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f"logs/Domain/{cli_args.domain}/parallel_test_script.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
for h in logging.getLogger().handlers:
    h.setFormatter(formatter)
logger = logging.getLogger(__name__)

# ---------- Config ----------
ALL_MODELS = [
    {
        "name": "qwen2.5:1.5b",
        "results_path": os.getenv(
            "Qwen2_5_1_5B_RESULTS_PATH",
            f"Final_Results/{cli_args.domain}/qwen2.5_1.5B/{cli_args.test_file}_results_iter_{cli_args.iteration}.json",
        ),
    },
    {
        "name": "llama3.2:1b",
        "results_path": os.getenv(
            "Llama3_2_1B_RESULTS_PATH",
            f"Final_Results/{cli_args.domain}/llama3.2_1B/{cli_args.test_file}_results_iter_{cli_args.iteration}.json",
        ),
    }
]

if cli_args.model == "all":
    selected_models = ALL_MODELS
else:
    selected_models = [m for m in ALL_MODELS if m["name"] == cli_args.model]
    if not selected_models:
        print(f"Model '{cli_args.model}' not found in config.")
        sys.exit(1)

CONFIG = {
    "OLLAMA_API": os.getenv("OLLAMA_API", "http://127.0.0.1:11434/api/generate"),
    "MODELS": selected_models,
    "DATASET_PATH": os.getenv(
        "DATASET_PATH",
        f"datasets/Domain/{cli_args.domain}/{cli_args.test_file}.json"
    ),
    "TIMEOUT": int(os.getenv("TIMEOUT", 60)),
    "MAX_RETRIES": int(os.getenv("MAX_RETRIES", 3)),
    "TEMPERATURE": float(os.getenv("TEMPERATURE", 0.3)),
    "MAX_TOKENS": int(os.getenv("MAX_TOKENS", 512)),
}

# ---------- Validation ----------
def validate_config():
    if not urlparse(CONFIG["OLLAMA_API"]).scheme:
        logger.error("Invalid OLLAMA_API URL")
        sys.exit(1)
    if not Path(CONFIG["DATASET_PATH"]).is_file():
        logger.error("Dataset not found")
        sys.exit(1)
    for m in CONFIG["MODELS"]:
        out = Path(m["results_path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            (out.parent / ".write_test").write_text("test")
            (out.parent / ".write_test").unlink()
        except (PermissionError, IOError) as e:
            logger.error("Cannot write to %s: %s", out.parent, e)
            sys.exit(1)

def check_ollama():
    try:
        r = requests.get("http://127.0.0.1:11434", timeout=5)
        if r.status_code == 200:
            logger.info("Ollama reachable")
            return True
        logger.error("Ollama check failed: %s", r.status_code)
        return False
    except requests.RequestException as e:
        logger.error("Ollama unreachable: %s", e)
        return False

# ---------- Helpers ----------
def get_process_tree_rss_mb() -> float:
    """Return RSS in MiB for the whole process tree (parent + children)."""
    try:
        parent = psutil.Process()
        children = parent.children(recursive=True)
        total_bytes = sum(p.memory_info().rss for p in [parent] + children)
        return total_bytes / 1024 / 1024
    except psutil.Error:
        return 0.0

# ---------- API ----------
@tenacity.retry(
    stop=tenacity.stop_after_attempt(CONFIG["MAX_RETRIES"]),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
    retry=tenacity.retry_if_exception_type(
        (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
    ),
    before_sleep=lambda rs: logger.warning(
        "Retry %d/%d – %s", rs.attempt_number, CONFIG["MAX_RETRIES"], rs.outcome.exception()
    ),
)
def query_ollama(prompt: str, model_name: str) -> Dict[str, Any]:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": CONFIG["TEMPERATURE"],
        "max_tokens": CONFIG["MAX_TOKENS"],
    }
    start = time.time()
    mem_before = get_process_tree_rss_mb()

    try:
        r = requests.post(CONFIG["OLLAMA_API"], json=payload, timeout=CONFIG["TIMEOUT"])
        latency_ms = (time.time() - start) * 1000
        mem_after = get_process_tree_rss_mb()
        memory_peak_mb = max(mem_before, mem_after)

        r.raise_for_status()
        data = r.json()

        prediction = data.get("response", "").strip()
        prompt_tokens = int(data.get("prompt_eval_count", 0))
        completion_tokens = int(data.get("eval_count", 0))
        total_tokens = prompt_tokens + completion_tokens
        throughput_tps = total_tokens / (latency_ms / 1000.0) if latency_ms else 0.0

        # Counts with fixed reference tokenizer (cross-model comparable)
        ref_prompt_tokens = len(REF_TOKENIZER.encode(prompt))
        ref_completion_tokens = len(REF_TOKENIZER.encode(prediction))
        ref_total_tokens = ref_prompt_tokens + ref_completion_tokens
        ref_throughput_tps = ref_total_tokens / (latency_ms / 1000.0) if latency_ms else 0.0

        return {
            "success": True,
            "prediction": prediction,
            "latency_ms": latency_ms,
            "memory_peak_mb": memory_peak_mb,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "throughput_tps": throughput_tps,
            "ref_prompt_tokens": ref_prompt_tokens,
            "ref_completion_tokens": ref_completion_tokens,
            "ref_total_tokens": ref_total_tokens,
            "ref_throughput_tps": ref_throughput_tps,
            "raw_response": data,
        }

    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        mem_after = get_process_tree_rss_mb()
        memory_peak_mb = max(mem_before, mem_after)
        logger.error("API call failed: %s", e)
        return {
            "success": False,
            "prediction": f"Error: {e}",
            "latency_ms": latency_ms,
            "memory_peak_mb": memory_peak_mb,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "throughput_tps": 0.0,
            "ref_prompt_tokens": 0,
            "ref_completion_tokens": 0,
            "ref_total_tokens": 0,
            "ref_throughput_tps": 0.0,
            "raw_response": {},
        }

# ---------- Evaluation ----------
import re

def evaluate_exact_match(predicted: str, expected: str) -> bool:
    predicted = predicted.lower().strip()
    expected = expected.lower().strip()
    for pat in [r"\s*cm²$", r"\s*m²$", r"\s*%$"]:
        predicted = re.sub(pat, "", predicted)
        expected = re.sub(pat, "", expected)
    try:
        pred_num = float(re.search(r"\d+\.?\d*", predicted).group())
        exp_num = float(re.search(r"\d+\.?\d*", expected).group())
        return abs(pred_num - exp_num) < 0.1
    except Exception:
        pass
    if "or" in expected or "/" in expected:
        exp_parts = (
            [p.strip() for p in expected.split("or")]
            if "or" in expected
            else [expected]
        )
        pred_parts = (
            [p.strip() for p in predicted.split("or")]
            if "or" in predicted
            else [predicted]
        )
        for ep in exp_parts:
            for pp in pred_parts:
                if ep == pp:
                    return True
    return predicted == expected

def evaluate_similarity(predicted: str, expected: str) -> float:
    return SequenceMatcher(None, predicted.lower(), expected.lower()).ratio()

def validate_task(task: Dict[str, Any]) -> bool:
    required = {"task_id", "prompt", "expected_answer", "evaluation_metric"}
    if not required.issubset(task):
        logger.error("Invalid task schema: %s", task)
        return False
    if task["evaluation_metric"] not in {
        "exact_match",
        "partial_correctness_for_reasoning",
        "correctness_with_explanation",
    }:
        logger.error("Invalid metric: %s", task["task_id"])
        return False
    return True

# ---------- Parallel ----------
def process_model(args):
    model_name, dataset, results_queue = args
    logger.info("Starting %s (%d tasks)", model_name, len(dataset))
    results = []
    for task in dataset:
        task_id = task["task_id"]
        prompt = task["prompt"]
        expected = task["expected_answer"]
        resp = query_ollama(task["prompt"], model_name)
        predicted = resp["prediction"]
        metric = task["evaluation_metric"]
        correct = False
        score = 0.0
        try:
            if metric == "exact_match":
                correct = evaluate_exact_match(predicted, task["expected_answer"])
                score = 1.0 if correct else 0.0
            else:
                score = evaluate_similarity(predicted, task["expected_answer"])
                correct = score > 0.8
        except Exception as e:
            logger.error("Evaluation error %s: %s", task["task_id"], e)

        results.append(
            {
                "task_id": task_id,
                "prompt": prompt,
                "expected": expected,
                "predicted": predicted,
                "correct": correct,
                "score": score,
                "metric": metric,
                "latency_ms": resp["latency_ms"],
                "memory_peak_mb": resp["memory_peak_mb"],
                "prompt_tokens": resp["prompt_tokens"],
                "completion_tokens": resp["completion_tokens"],
                "total_tokens": resp["total_tokens"],
                "throughput_tps": resp["throughput_tps"],
                "ref_prompt_tokens": resp["ref_prompt_tokens"],
                "ref_completion_tokens": resp["ref_completion_tokens"],
                "ref_total_tokens": resp["ref_total_tokens"],
                "ref_throughput_tps": resp["ref_throughput_tps"],
                "success": resp["success"],
            }
        )
    results_queue[model_name] = results
    logger.info("Finished %s", model_name)

# ---------- Save / Summarise ----------
def save_results(model_name: str, results: List[Dict[str, Any]], path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info("Saved %s to %s", model_name, path)

def summarize(model_name: str, results: List[Dict[str, Any]]):
    total = len(results)
    succ = [r for r in results if r["success"]]
    correct = sum(r["correct"] for r in succ)
    accuracy = correct / total * 100 if total else 0
    avg_lat = sum(r["latency_ms"] for r in succ) / len(succ) if succ else 0
    avg_mem = sum(r["memory_peak_mb"] for r in succ) / len(succ) if succ else 0
    avg_tps = sum(r["throughput_tps"] for r in succ) / len(succ) if succ else 0
    total_tok = sum(r["total_tokens"] for r in succ)
    logger.info("=== %s summary ===", model_name)
    logger.info("Tasks: %d | Success: %d | Accuracy: %.2f%%", total, len(succ), accuracy)
    logger.info("Avg latency: %.2f ms", avg_lat)
    logger.info("Avg memory-peak: %.2f MB", avg_mem)
    logger.info("Avg throughput: %.2f t/s", avg_tps)
    logger.info("Total tokens processed: %d", total_tok)

# ---------- Main ----------
def main():
    validate_config()
    if not check_ollama():
        sys.exit(1)
    try:
        with open(CONFIG["DATASET_PATH"], encoding="utf-8") as f:
            dataset = json.load(f)
    except Exception as e:
        logger.error("Cannot load dataset: %s", e)
        sys.exit(1)

    dataset = [t for t in dataset if validate_task(t)]
    if not dataset:
        logger.error("No valid tasks")
        sys.exit(1)

    manager = Manager()
    results_queue = manager.dict()
    pool_args = [(m["name"], dataset, results_queue) for m in CONFIG["MODELS"]]

    with Pool(processes=len(CONFIG["MODELS"])) as pool:
        pool.map(process_model, pool_args)

    for m in CONFIG["MODELS"]:
        model_name = m["name"]
        if model_name not in results_queue:
            logger.error("No results for %s", model_name)
            continue
        results = results_queue[model_name]
        save_results(model_name, results, m["results_path"])
        summarize(model_name, results)

if __name__ == "__main__":
    main()