import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
from models import Session, Cycle

def get_cycle_data():
    session = Session()
    cycles = session.query(Cycle).order_by(Cycle.start_date).all()
    session.close()
    
    if len(cycles) < 2:
        return None, None
    
    dates = [cycle.start_date for cycle in cycles]
    intervals = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
    return dates[1:], intervals

def generate_cycle_length_plot():
    ...

def generate_distribution_plot():
    ...
