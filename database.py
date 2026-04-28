import pandas as pd
import os
from datetime import datetime

DB_FILE = 'training_data.csv'

def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=[
            'Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Attendees', 'Status'
        ])
        df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')

def save_registration(dept, team, session, content, date, timeslot, attendees):
    df = pd.read_csv(DB_FILE)
    new_entry = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Department': dept,
        'Team': team,
        'Session': session,
        'Content': content,
        'Date': date.strftime("%Y-%m-%d"),
        'TimeSlot': timeslot,
        'Attendees': attendees,
        'Status': 'Pending'
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')

def delete_registration(index):
    df = pd.read_csv(DB_FILE)
    if 0 <= index < len(df):
        df = df.drop(index)
        df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
        return True
    return False

def get_registrations():
    if not os.path.exists(DB_FILE):
        init_db()
    return pd.read_csv(DB_FILE)
