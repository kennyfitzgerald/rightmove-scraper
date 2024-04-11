import pandas as pd


def filter_inactive_records(records):
    filtered_records = [record for record in records if record.get("active") == 1]
    return filtered_records


def google_sheet_to_json(google_sheet_id, gid):
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?gid={gid}&format=csv"
    )
    records = df.to_dict(orient="records")
    filtered_records = filter_inactive_records(records)
    return filtered_records
