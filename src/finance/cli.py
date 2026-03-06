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