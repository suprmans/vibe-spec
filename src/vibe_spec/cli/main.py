"""vibe-spec CLI entry point."""

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="vibe-spec",
    help="AI-first business specification framework.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def validate(
    artefact_type: str = typer.Argument(help="Artefact type: context, vibe_fingerprint"),
    path: str = typer.Argument(help="Path to the JSON artefact file"),
) -> None:
    """Validate a vibe-spec artefact against CONSTITUTION.md rules."""
    from pathlib import Path

    from vibe_spec.schemas.validate import validate_file

    violations = validate_file(artefact_type, Path(path))
    if not violations:
        console.print(Panel("[green]✓ Artefact passes all constitutional checks[/green]", title="Validation"))
    else:
        console.print(Panel("\n".join(f"[red]✗ {v}[/red]" for v in violations), title="Violations"))
        raise typer.Exit(code=1)


@app.command()
def score(
    requirements_completeness: float = typer.Option(..., help="0.0–1.0"),
    gap_coverage: float = typer.Option(..., help="0.0–1.0"),
    stakeholder_completeness: float = typer.Option(..., help="0.0–1.0"),
    vibe_confidence_avg: float = typer.Option(..., help="0.0–1.0"),
    risk_coverage: float = typer.Option(..., help="0.0–1.0"),
) -> None:
    """Compute spec_health composite score."""
    from vibe_spec.scoring.spec_health import SpecHealthInput, compute_spec_health

    inputs = SpecHealthInput(
        requirements_completeness=requirements_completeness,
        gap_coverage=gap_coverage,
        stakeholder_completeness=stakeholder_completeness,
        vibe_confidence_avg=vibe_confidence_avg,
        risk_coverage=risk_coverage,
    )
    result = compute_spec_health(inputs)

    colour = "green" if result.score >= 0.80 else "yellow" if result.score >= 0.60 else "red"
    console.print(
        Panel(
            f"[{colour}]spec_health: {result.score:.4f} — {result.status}[/{colour}]\n\n{result.recommendation}",
            title="Spec Health",
        )
    )


if __name__ == "__main__":
    app()
