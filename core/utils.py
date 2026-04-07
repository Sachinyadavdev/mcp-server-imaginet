from datetime import datetime, date, timedelta

def serialize_sql_row(row):
    """Helper to convert SQL dates and timedeltas into JSON-friendly format"""
    for key, val in row.items():
        if isinstance(val, (datetime, date)):
            row[key] = val.isoformat()
        elif isinstance(val, timedelta):
            row[key] = str(val)
    return row
