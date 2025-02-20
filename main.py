import os
import click
from datetime import datetime, timedelta
from data_viz import generate_cycle_length_plot, generate_distribution_plot
from models import *

@click.group()
def cli():
    pass

@cli.command()
def init_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    click.echo("Database initialized successfully.")

@cli.command()
@click.argument("start_date")
@click.argument("name")
def add(start_date, name):
    """Add a new period start date (YYYY-MM-DD) of a person"""
    session = Session()
    try:
        date = datetime.strptime(start_date, "%Y-%m-%d").date()
        existing_cycle = session.query(Cycle).filter_by(
                start_date=date,
                name=name
            ).first()
        if existing_cycle:
            click.echo("Error: A cycle with this date and name already exists.")
            session.close()
            return
        cycle = Cycle(start_date=date, name=name)
        session.add(cycle)
        session.commit()
        click.echo(f"Recorded cycle\n{cycle}")
    except ValueError:
        click.echo("Error: Invalid date format. Please use YYYY-MM-DD.")
    except Exception as e:
        session.rollback()  # Rollback the session on failure
        click.echo(f"Error: {e}")
    finally:
        session.close()

@cli.command()
def visualize():
    """Generate and save cycle visualizations"""
    ...

@cli.command()
@click.argument("name")
def predict():
    """Predict the next period start date based on average cycle length."""
    session = Session()
    cycles = session.query(Cycle).filter_by(name=name).order_by(Cycle.start_date).all()
    if len(cycles) < 2:
        click.echo("Not enough data to predict the next cycle.")
        return
    total_days = sum(
        (cycles[i + 1].start_date - cycles[i].start_date).days
        for i in range(len(cycles) - 1)
    )
    average_cycle_length = total_days / (len(cycles) - 1)
    last_cycle_start = cycles[-1].start_date
    next_cycle_start = last_cycle_start + timedelta(days=average_cycle_length)
    click.echo(f"Based on an average cycle length of {average_cycle_length:.1f} days,")
    click.echo(f"the next period is predicted to start on {next_cycle_start}.")
    session.close()

@cli.command()
def history():
    """View recorded period history."""
    session = Session()
    cycles = session.query(Cycle).order_by(Cycle.start_date).all()
    if not cycles:
        click.echo("No period history available.")
        return
    click.echo("Period History:")
    click.echo("Start Date\tName")
    for cycle in cycles:
        click.echo(f"{cycle.start_date}\t{cycle.name}")
    session.close()

if __name__ == "__main__":
    cli()
