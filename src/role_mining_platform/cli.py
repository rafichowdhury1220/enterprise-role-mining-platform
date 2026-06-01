from __future__ import annotations

import typer
from rich.console import Console

from .pipeline import RoleMiningPipeline
from .role_suggestions import RoleSuggestionEngine

app = typer.Typer()
console = Console()


@app.command()
def analyze(source: str | None = typer.Option(None, help="Path to a CSV entitlement dataset.")) -> None:
    """Analyze IAM access data and show role mining results."""
    pipeline = RoleMiningPipeline(source)
    df = pipeline.load()
    results = pipeline.analyze()

    console.rule("IAM Role Mining Analysis")
    console.print(f"Loaded {len(df)} entitlement assignments.")
    console.print(f"Detected {len(results['redundant_entitlements'])} entitlements flagged for review.")
    console.print(f"Discovered {len(results['role_clusters'])} candidate role clusters.")


@app.command()
def suggest(source: str | None = typer.Option(None, help="Path to a CSV entitlement dataset.")) -> None:
    """Print suggested role definitions based on clustering."""
    pipeline = RoleMiningPipeline(source)
    pipeline.load()
    results = pipeline.analyze()
    engine = RoleSuggestionEngine()
    suggestions = engine.suggest_roles(results["role_clusters"])
    engine.print_suggestions(suggestions)


@app.command()
def summary(source: str | None = typer.Option(None, help="Path to a CSV entitlement dataset.")) -> None:
    """Display a high-level summary of the IAM architecture and risks."""
    pipeline = RoleMiningPipeline(source)
    df = pipeline.load()
    results = pipeline.analyze()

    console.rule("IAM Architecture Summary")
    console.print(f"Users: {df['user_id'].nunique()}")
    console.print(f"Applications: {df['application'].nunique()}")
    console.print(f"Unique entitlements: {df['entitlement_normalized'].nunique()}")
    console.print(f"Candidate roles: {len(results['role_clusters'])}")
    console.print("Review high-frequency entitlements for potential privilege creep.")


if __name__ == "__main__":
    app()
