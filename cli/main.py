"""Command-line interface for nti-benchmark."""


import json
from pathlib import Path


import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


from runner.run_benchmark import run_all, save_results
from runner.attestation import sign_benchmark, verify_benchmark


console = Console()




@click.group()
@click.version_option()
def main():
    """nti-benchmark: verifiable security benchmark for AI agent frameworks."""
    pass




@main.command()
@click.option("--output", "-o", default="results", help="Output directory")
@click.option("--sign/--no-sign", default=True, help="Sign results with Dilithium5")
def run(output, sign):
    """Run the benchmark across all frameworks."""
    console.print("[bold cyan]Running NTI Benchmark...[/bold cyan]\n")


    def progress(i, total, name):
        console.print(f"[{i+1}/{total}] Running: {name}")


    data = run_all(progress_cb=progress)


    if sign:
        data = sign_benchmark(data)


    path = save_results(data, output)


    table = Table(title="NTI Benchmark Results")
    table.add_column("Framework", style="cyan")
    table.add_column("Bare Score", justify="right")
    table.add_column("With NTI", justify="right")
    table.add_column("Delta", justify="right")


    for r in data["results"]:
        delta_color = "green" if r["delta"] > 0 else "red"
        table.add_row(
            r["framework_name"],
            f"{r['bare']['score']}/100",
            f"[green]{r['with_nti']['score']}/100[/green]",
            f"[{delta_color}]+{r['delta']}[/{delta_color}]",
        )


    console.print()
    console.print(table)
    console.print()
    console.print(f"Report saved: {path}")
    if sign:
        console.print("[green]Signed with Dilithium5[/green]")




@main.command()
@click.argument("path", type=click.Path(exists=True))
def verify(path):
    """Verify a signed benchmark report offline."""
    data = json.loads(Path(path).read_text())
    if verify_benchmark(data):
        console.print(Panel.fit("[green]VALID[/green]", title="Verification"))
    else:
        console.print(Panel.fit("[red]INVALID[/red]", title="Verification"))




if __name__ == "__main__":
    main()
