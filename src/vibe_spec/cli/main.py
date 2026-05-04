"""vibe-spec CLI entry point.

Commands are invoked by Claude agents via Bash inside skill instructions.
All outputs are machine-readable (JSON) by default so agents can parse them.
"""

import json

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
    artefact_type: str = typer.Argument(
        help="context | vibe_fingerprint | requirements | stakeholder-map | gap-analysis"
    ),
    path: str = typer.Argument(help="Path to the artefact file"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Validate an artefact against CONSTITUTION.md rules."""
    from pathlib import Path

    from vibe_spec.schemas.validate import validate_file

    violations = validate_file(artefact_type, Path(path))
    if json_output:
        typer.echo(json.dumps({"valid": len(violations) == 0, "violations": violations}))
        if violations:
            raise typer.Exit(code=1)
        return

    if not violations:
        console.print(
            Panel(
                "[green]✓ Passes all constitutional checks[/green]",
                title=f"Validate: {artefact_type}",
            )
        )
    else:
        console.print(Panel("\n".join(f"[red]✗ {v}[/red]" for v in violations), title="Violations"))
        raise typer.Exit(code=1)


@app.command(name="score-story")
def score_story(
    text: str = typer.Option(..., help="User story text"),
    ac: list[str] = typer.Option(..., help="Acceptance criterion (repeat for multiple)"),
    has_dependency: bool = typer.Option(False, help="Story depends on another incomplete story"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Score a user story against INVEST criteria and detect ambiguity."""
    from vibe_spec.scoring.invest import score_story as _score

    invest, ambiguity = _score(
        story_text=text,
        acceptance_criteria=list(ac),
        has_dependency=has_dependency,
    )

    result = {
        "invest_score": round(invest.average, 4),
        "passes": invest.passes,
        "criteria": {
            "independent": invest.independent,
            "negotiable": invest.negotiable,
            "valuable": invest.valuable,
            "estimable": invest.estimable,
            "small": invest.small,
            "testable": invest.testable,
        },
        "ambiguity_flag": ambiguity.flag_count,
        "weasel_words": ambiguity.weasel_words,
        "unmeasurable_phrases": ambiguity.unmeasurable_phrases,
        "ac_coverage": len(ac),
    }

    if json_output:
        typer.echo(json.dumps(result))
        if not invest.passes:
            raise typer.Exit(code=1)
        return

    criteria: dict[str, float] = {
        "independent": invest.independent,
        "negotiable": invest.negotiable,
        "valuable": invest.valuable,
        "estimable": invest.estimable,
        "small": invest.small,
        "testable": invest.testable,
    }
    colour = "green" if invest.passes else "red"
    detail = "\n".join(f"  {k}: {v:.2f}" for k, v in criteria.items())
    flags = (
        f"\nAmbiguity flags ({ambiguity.flag_count}): {ambiguity.weasel_words + ambiguity.unmeasurable_phrases}"
        if ambiguity.flag_count
        else ""
    )
    console.print(
        Panel(
            f"[{colour}]invest_score: {result['invest_score']:.4f} — {'PASS' if invest.passes else 'FAIL'}[/{colour}]\n{detail}{flags}",
            title="Score Story",
        )
    )
    if not invest.passes:
        raise typer.Exit(code=1)


@app.command(name="score-nfr")
def score_nfr(
    category: str = typer.Argument(
        help="NFR category: performance | security | availability | scalability | usability | compliance | maintainability | interoperability | data_privacy"
    ),
    criterion: str = typer.Option(..., help="The measurable criterion text to score"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Score an NFR criterion for measurability. Blocked if score < 0.50."""
    from vibe_spec.scoring.nfr import NFR_CATEGORIES, score_nfr_measurability

    if category not in NFR_CATEGORIES:
        console.print(f"[red]Unknown category '{category}'. Valid: {sorted(NFR_CATEGORIES)}[/red]")
        raise typer.Exit(code=1)

    result = score_nfr_measurability(category, criterion)

    output = {
        "category": category,
        "measurability_score": result.score,
        "passes": result.passes,
        "blocked": result.blocked,
        "metric_signals_found": result.metric_signals_found,
        "vague_signals_found": result.vague_signals_found,
        "feedback": result.feedback,
    }

    if json_output:
        typer.echo(json.dumps(output))
        if result.blocked:
            raise typer.Exit(code=1)
        return

    colour = "green" if result.passes else "red"
    console.print(
        Panel(
            f"[{colour}]{result.feedback}[/{colour}]",
            title=f"Score NFR: {category}",
        )
    )
    if result.blocked:
        raise typer.Exit(code=1)


@app.command(name="score-gap")
def score_gap(
    trace_id: str = typer.Option(..., help="Traceability ID: REQ-XXX or PAIN-XXX"),
    effort: str = typer.Option(..., help="Effort estimate: XS | S | M | L | XL"),
    impact: float = typer.Option(..., help="Impact score 0.0–10.0"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Compute gap priority tier and quick_win_flag from impact and effort."""
    valid_efforts = {"XS", "S", "M", "L", "XL"}
    if effort not in valid_efforts:
        console.print(f"[red]Invalid effort '{effort}'. Must be one of: {valid_efforts}[/red]")
        raise typer.Exit(code=1)

    quick_win = impact >= 6.0 and effort in {"XS", "S"}

    if quick_win:
        priority_tier = 1
        tier_label = "Quick win"
    elif impact >= 7.0 and effort in {"M", "L"}:
        priority_tier = 2
        tier_label = "Strategic bet"
    elif 3.0 <= impact < 7.0 and effort in {"XS", "S"}:
        priority_tier = 3
        tier_label = "Fill-in"
    else:
        priority_tier = 4
        tier_label = "Deprioritise"

    result = {
        "trace_id": trace_id,
        "impact": impact,
        "effort": effort,
        "quick_win_flag": quick_win,
        "priority_tier": priority_tier,
        "priority_label": tier_label,
    }

    if json_output:
        typer.echo(json.dumps(result))
        return

    colour = "green" if priority_tier <= 2 else "yellow" if priority_tier == 3 else "dim"
    console.print(
        Panel(
            f"[{colour}]Priority {priority_tier}: {tier_label}[/{colour}]\n"
            f"quick_win: {quick_win} | impact: {impact} | effort: {effort}",
            title=f"Score Gap: {trace_id}",
        )
    )


@app.command(name="spec-health")
def spec_health(
    requirements_completeness: float = typer.Option(..., help="0.0–1.0"),
    gap_coverage: float = typer.Option(..., help="0.0–1.0"),
    stakeholder_completeness: float = typer.Option(..., help="0.0–1.0"),
    vibe_confidence_avg: float = typer.Option(..., help="0.0–1.0"),
    risk_coverage: float = typer.Option(..., help="0.0–1.0"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
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

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "spec_health": result.score,
                    "status": result.status,
                    "recommendation": result.recommendation,
                    "components": result.component_scores,
                    "weighted": result.weighted_contributions,
                }
            )
        )
        return

    colour = "green" if result.score >= 0.80 else "yellow" if result.score >= 0.60 else "red"
    console.print(
        Panel(
            f"[{colour}]spec_health: {result.score:.4f} — {result.status}[/{colour}]\n\n{result.recommendation}",
            title="Spec Health",
        )
    )


@app.command(name="score-risk")
def score_risk(
    likelihood: float = typer.Option(..., help="Likelihood 0.0–10.0"),
    impact: float = typer.Option(..., help="Impact 0.0–10.0"),
    category: str = typer.Option(..., help="Risk category"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Compute risk score and classification from likelihood × impact."""
    from vibe_spec.scoring.risk import RISK_CATEGORIES, compute_risk_score

    if category not in RISK_CATEGORIES:
        console.print(f"[red]Unknown category '{category}'. Valid: {sorted(RISK_CATEGORIES)}[/red]")
        raise typer.Exit(code=1)

    try:
        result = compute_risk_score(likelihood, impact)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1) from e

    output = {
        "likelihood": result.likelihood,
        "impact": result.impact,
        "risk_score": result.risk_score,
        "classification": result.classification,
        "category": category,
    }

    if json_output:
        typer.echo(json.dumps(output))
        return

    colour = (
        "red"
        if result.classification == "critical"
        else "yellow"
        if result.classification == "high"
        else "blue"
        if result.classification == "medium"
        else "dim"
    )
    console.print(
        Panel(
            f"[{colour}]{result.classification.upper()} — risk_score: {result.risk_score:.2f}[/{colour}]\n"
            f"likelihood: {likelihood} × impact: {impact} / 10",
            title=f"Score Risk: {category}",
        )
    )


@app.command(name="write-artefact")
def write_artefact(
    artefact_type: str = typer.Argument(
        help="Artefact type (e.g. context, requirements, risk-register)"
    ),
    output_dir: str = typer.Argument(help="Output directory path"),
    data: str = typer.Argument(help="JSON string of artefact data"),
    version: str = typer.Option("0.1", help="Artefact version"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON for agent parsing"),
) -> None:
    """Write a versioned artefact file to the output directory."""
    import json as json_module
    from pathlib import Path

    from vibe_spec.output.artefact import write_artefact as _write

    try:
        parsed = json_module.loads(data)
    except json_module.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON data: {e}[/red]")
        raise typer.Exit(code=1) from e

    path = _write(Path(output_dir), artefact_type, parsed, version)

    if json_output:
        typer.echo(json.dumps({"path": str(path), "artefact_type": artefact_type}))
        return

    console.print(
        Panel(f"[green]Written: {path}[/green]", title=f"Write Artefact: {artefact_type}")
    )


if __name__ == "__main__":
    app()
