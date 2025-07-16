from mcp.server.fastmcp import FastMCP
import pandas as pd
import re
import os

mcp = FastMCP("llm_eval_insights")

@mcp.tool()
def list_models() -> list[str]:
    """Returns a list of unique models in the dataset."""
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
        df.columns = df.columns.str.replace('-', '_').str.lower()
        return df["model"].dropna().unique().tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return []
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return []

@mcp.tool()
def list_domains() -> list[str]:
    """Returns a list of unique domains in the dataset. Domains broadly classify the areas in which model is tested. A domain has multiple sub domains/categories"""
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
        df.columns = df.columns.str.replace('-', '_').str.lower()
        return df["domain"].dropna().unique().tolist()
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return []
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return []

@mcp.tool()
def list_sub_domains(domain: str) -> list[str]:
    """Returns a list of unique sub-domains for a given domain. Takes in input a Domain available in the list returned by list_domains"""
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
        df.columns = df.columns.str.replace('-', '_').str.lower()
        subdomains = df[df["domain"] == domain]["sub_domain"].dropna().unique().tolist()
        print(f"Sub-domains for domain={domain}: {subdomains}")
        return subdomains
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return []
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return []

@mcp.tool()
def get_metric_domain(model: str, domain: str) -> dict:
    """
    Get average metrics for a given model and domain, averaging across all sub-domains.

    Args:
        model: The model name, which was returned by "list_models" tool
        domain: The domain name, which was returned by "list_domains" tool

    Returns:
        Dictionary of average metrics (accuracy, latency_ms, memory_mb, cpu_ms, etc.)
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return {}
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return {}

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return {}

    # Filter DataFrame
    query = (df["model"] == model) & (df["domain"] == domain)
    filtered_df = df[query]
    if filtered_df.empty:
        print(f"No matching rows for model={model}, domain={domain}")
        return {}

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Define numeric columns
    numeric_cols = [
        "accuracy", "latency_ms", "memory_mb", "cpu_ms", "total_duration_ms",
        "load_duration_ms", "prompt_eval_count", "prompt_eval_duration_ms",
        "eval_count", "eval_duration_ms"
    ]
    missing_cols = [col for col in numeric_cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing numeric columns: {missing_cols}")
        numeric_cols = [col for col in numeric_cols if col in df.columns]

    # Clean numeric columns
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        cleaned_df = filtered_df[numeric_cols].apply(lambda col: col.apply(clean_metric))
        averages = cleaned_df.mean().to_dict()
        return averages
    except Exception as e:
        print(f"Error cleaning numeric columns: {e}")
        return {}

@mcp.tool()
def get_metric_domain_subdomain(model: str, domain: str, sub_domain: str) -> dict:
    """
    Get metrics for a given model, domain, and specific sub-domain.

    Args:
        model: The model name, which was returned by "list_models" tool
        domain: The domain name, which was returned by "list_domains" tool
        sub_domain: The sub-domain name, which was returned by "list_sub_domains" tool

    Returns:
        Dictionary of metrics (accuracy, latency_ms, memory_mb, cpu_ms, etc.)
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return {}
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return {}

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain', 'sub_domain']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return {}

    # Handle list input for sub_domain
    if isinstance(sub_domain, list):
        sub_domain = sub_domain[0] if sub_domain else None
    if not sub_domain:
        print("Error: sub_domain must be a non-empty string")
        return {}

    # Filter DataFrame
    query = (df["model"] == model) & (df["domain"] == domain) & (df["sub_domain"].str.lower() == sub_domain.lower()) & (df["sub_domain"].notna())
    filtered_df = df[query]
    if filtered_df.empty:
        print(f"No matching rows for model={model}, domain={domain}, sub_domain={sub_domain}")
        return {}

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Define numeric columns
    numeric_cols = [
        "accuracy", "latency_ms", "memory_mb", "cpu_ms", "total_duration_ms",
        "load_duration_ms", "prompt_eval_count", "prompt_eval_duration_ms",
        "eval_count", "eval_duration_ms"
    ]
    missing_cols = [col for col in numeric_cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing numeric columns: {missing_cols}")
        numeric_cols = [col for col in numeric_cols if col in df.columns]

    # Clean numeric columns
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        cleaned_df = filtered_df[numeric_cols].apply(lambda col: col.apply(clean_metric))
        # Return first row (no averaging) if only one row exists
        if len(cleaned_df) == 1:
            return cleaned_df.iloc[0].to_dict()
        # Otherwise, average multiple rows
        averages = cleaned_df.mean().to_dict()
        return averages
    except Exception as e:
        print(f"Error cleaning numeric columns: {e}")
        return {}

@mcp.tool()
def compare_models_domain(domain: str) -> dict:
    """
    Compare models for a given domain, averaging across all sub-domains.

    Args:
        domain: The domain to compare all the models returned by "list_models" tool

    Returns:
        Dictionary mapping each model name to their average accuracy
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return {}
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return {}

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain', 'accuracy']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return {}

    # Filter DataFrame
    filtered_df = df[df["domain"] == domain]
    if filtered_df.empty:
        print(f"No matching rows for domain={domain}")
        return {}

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Clean accuracy column
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
        filtered_df.loc[:, "accuracy"] = filtered_df["accuracy"].apply(clean_metric)
        comparison = filtered_df.groupby("model")["accuracy"].mean().to_dict()
        return comparison
    except Exception as e:
        print(f"Error processing accuracy: {e}")
        return {}

@mcp.tool()
def compare_models_domain_subdomain(domain: str, sub_domain: str) -> dict:
    """
    Compare models for a given domain and specific sub-domain.

    Args:
        domain: The domain to compare models in
        sub_domain: The sub-domain to filter by

    Returns:
        Dictionary mapping each model name to their average accuracy
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return {}
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return {}

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain', 'sub_domain', 'accuracy']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return {}

    # Handle list input for sub_domain
    if isinstance(sub_domain, list):
        sub_domain = sub_domain[0] if sub_domain else None
    if not sub_domain:
        print("Error: sub_domain must be a non-empty string")
        return {}

    # Filter DataFrame
    query = (df["domain"] == domain) & (df["sub_domain"].str.lower() == sub_domain.lower()) & (df["sub_domain"].notna())
    filtered_df = df[query]
    if filtered_df.empty:
        print(f"No matching rows for domain={domain}, sub_domain={sub_domain}")
        return {}

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Clean accuracy column
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
        filtered_df.loc[:, "accuracy"] = filtered_df["accuracy"].apply(clean_metric)
        comparison = filtered_df.groupby("model")["accuracy"].mean().to_dict()
        return comparison
    except Exception as e:
        print(f"Error processing accuracy: {e}")
        return {}

@mcp.tool()
def models_meeting_threshold_domain(domain: str, threshold: float) -> list[str]:
    """
    List models whose average accuracy meets or exceeds a threshold in a domain.

    Args:
        domain: The domain name
        threshold: Accuracy threshold

    Returns:
        List of model names
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return []
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return []

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain', 'accuracy']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return []

    # Filter DataFrame
    filtered_df = df[df["domain"] == domain]
    if filtered_df.empty:
        print(f"No matching rows for domain={domain}")
        return []

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Clean accuracy column
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
        filtered_df.loc[:, "accuracy"] = filtered_df["accuracy"].apply(clean_metric)
        avg_accuracy = filtered_df.groupby("model")["accuracy"].mean()
        models = avg_accuracy[avg_accuracy >= threshold].index.tolist()
        return models
    except Exception as e:
        print(f"Error processing accuracy: {e}")
        return []

@mcp.tool()
def models_meeting_threshold_domain_subdomain(domain: str, sub_domain: str, threshold: float) -> list[str]:
    """
    List models whose average accuracy meets or exceeds a threshold in a specific domain and sub-domain.

    Args:
        domain: The domain name
        sub_domain: The sub-domain name
        threshold: Accuracy threshold

    Returns:
        List of model names
    """
    try:
        df = pd.read_csv(os.getenv("final.csv", "final.csv"))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {os.getenv('final.csv', 'final.csv')}")
        return []
    except pd.errors.ParserError:
        print("Error: Failed to parse CSV file")
        return []

    # Normalize column names
    df.columns = df.columns.str.replace('-', '_').str.lower()
    required_cols = ['model', 'domain', 'sub_domain', 'accuracy']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Required columns {required_cols} not found in CSV")
        return []

    # Handle list input for sub_domain
    if isinstance(sub_domain, list):
        sub_domain = sub_domain[0] if sub_domain else None
    if not sub_domain:
        print("Error: sub_domain must be a non-empty string")
        return []

    # Filter DataFrame
    query = (df["domain"] == domain) & (df["sub_domain"].str.lower() == sub_domain.lower()) & (df["sub_domain"].notna())
    filtered_df = df[query]
    if filtered_df.empty:
        print(f"No matching rows for domain={domain}, sub_domain={sub_domain}")
        return []

    # Debug: Print filtered rows
    print("Filtered DataFrame rows:")
    print(filtered_df.to_string())

    # Clean accuracy column
    def clean_metric(value):
        if isinstance(value, str):
            match = re.match(r'[\d.]+', value)
            return float(match.group()) if match else 0.0
        return float(value) if pd.notna(value) else 0.0

    try:
        filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
        filtered_df.loc[:, "accuracy"] = filtered_df["accuracy"].apply(clean_metric)
        avg_accuracy = filtered_df.groupby("model")["accuracy"].mean()
        models = avg_accuracy[avg_accuracy >= threshold].index.tolist()
        return models
    except Exception as e:
        print(f"Error processing accuracy: {e}")
        return []

if __name__ == "__main__":
    mcp.run(transport="stdio")

