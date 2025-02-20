import os
import click
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Cycle(Base):
    __tablename__ = 'cycles'
    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('start_date')
def add(start_date):
    """Add a new period start date (YYYY-MM-DD)."""
    session = Session()
    try:
        date = datetime.strptime(start_date, "%Y-%m-%d").date()
        cycle = Cycle(start_date=date)
        session.add(cycle)
        session.commit()
        click.echo(f"Recorded cycle starting on {start_date}.")
    except ValueError:
        click.echo("Error: Invalid date format. Please use YYYY-MM-DD.")
    finally:
        session.close()

@cli.command()
def predict():
    """Predict the next period start date based on average cycle length."""
    session = Session()
    cycles = session.query(Cycle).order_by(Cycle.start_date).all()
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
    for cycle in cycles:
        click.echo(f"- {cycle.start_date}")
    session.close()

if __name__ == "__main__":
    cli()
