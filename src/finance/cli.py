import typer
from rich.console import Console
from rich.table import Table
from rich import box
from finance.tracker import FinanceTracker

app = typer.Typer(help="Personal Finance Tracker")
console = Console()
tracker = FinanceTracker()


@app.command()
def add(
    amount: float = typer.Option(..., prompt="Amount"),
    category: str = typer.Option(..., prompt="Category"),
    type: str = typer.Option(..., prompt="Type (income/expense)"),
    description: str = typer.Option("", prompt="Description (optional)"),
):
    """Add a new income or expense record."""
    record = tracker.add(amount, category, type, description)
    console.print(f"[green]✓ Added:[/green] {record}")


@app.command()
def summary():
    """Show balance, total income and expenses."""
    table = Table(box=box.ROUNDED, show_header=False)
    table.add_column(style="bold")
    table.add_column(justify="right")

    table.add_row("Total Income",   f"[green]{tracker.total_income():.2f}[/green]")
    table.add_row("Total Expenses", f"[red]{tracker.total_expense():.2f}[/red]")
    table.add_row("Balance",        f"[bold]{tracker.balance():.2f}[/bold]")

    console.print(table)


@app.command()
def categories(
    type: str = typer.Option("expense", help="income or expense"),
):
    """Show spending breakdown by category."""
    data = tracker.by_category(type)
    table = Table(title=f"Category Report ({type})", box=box.ROUNDED)
    table.add_column("Category")
    table.add_column("Amount", justify="right")

    for cat, amount in data.items():
        table.add_row(cat, f"{amount:.2f}")

    console.print(table)


@app.command()
def monthly():
    """Show monthly income and expense summary."""
    data = tracker.by_month()
    table = Table(title="Monthly Summary", box=box.ROUNDED)
    table.add_column("Month")
    table.add_column("Income",  justify="right", style="green")
    table.add_column("Expenses", justify="right", style="red")
    table.add_column("Net",     justify="right")

    for month, values in data.items():
        diff = values["income"] - values["expense"]
        color = "green" if diff >= 0 else "red"
        table.add_row(
            month,
            f"{values['income']:.2f}",
            f"{values['expense']:.2f}",
            f"[{color}]{diff:.2f}[/{color}]",
        )

    console.print(table)


@app.command()
def list():
    """List all records with index numbers."""
    records = tracker.all()
    if not records:
        console.print("[yellow]No records found.[/yellow]")
        return
    table = Table(title="All Records", box=box.ROUNDED)
    table.add_column("Index", justify="right", style="dim")
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Amount", justify="right")
    table.add_column("Description")

    for i, r in enumerate(records):
        color = "green" if r["type"] == "income" else "red"
        table.add_row(
            str(i),
            r["date"],
            f"[{color}]{r['type']}[/{color}]",
            r["category"],
            f"[{color}]{r['amount']:.2f}[/{color}]",
            r["description"] or "-",
        )
    console.print(table)


@app.command()
def delete(
    index: int = typer.Option(..., prompt="Index to delete"),
):
    """Delete a record by its index (use 'list' to see indexes)."""
    try:
        record = tracker.delete(index)
        console.print(f"[red]✓ Deleted:[/red] {record}")
    except IndexError as e:
        console.print(f"[red]Error:[/red] {e}")


@app.command()
def filter(
    start: str = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(None, help="End date (YYYY-MM-DD)"),
):
    """Filter records by date range."""
    from datetime import date as d
    start_date = d.fromisoformat(start) if start else None
    end_date   = d.fromisoformat(end)   if end   else None
    records = tracker.filter_by_date(start_date, end_date)

    if not records:
        console.print("[yellow]No records found.[/yellow]")
        return

    table = Table(title="Filtered Records", box=box.ROUNDED)
    table.add_column("Date")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Amount", justify="right")
    table.add_column("Description")

    for r in records:
        color = "green" if r["type"] == "income" else "red"
        table.add_row(
            r["date"],
            f"[{color}]{r['type']}[/{color}]",
            r["category"],
            f"[{color}]{r['amount']:.2f}[/{color}]",
            r["description"] or "-",
        )
    console.print(table)


@app.command()
def export(
    path: str = typer.Option("finance_export.csv", help="Output file path"),
):
    """Export all records to a CSV file."""
    tracker.export_csv(path)
    console.print(f"[green]✓ Exported to {path}[/green]")