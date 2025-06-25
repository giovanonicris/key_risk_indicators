import pandas as pd
import os
from datetime import datetime, timedelta

# set up
kri_id = 105
input_file = "acled_geopolitical_tensions/acled_us_events.csv"  # download from ACLED manually
output_dir = "acled_geopolitics"
output_file = os.path.join(output_dir, "acled_us_geopolitical_tension_weekly.csv")
tension_event_types = [
    "Protests",
    "Riots",
    "Violence against civilians",
    "Explosions/Remote violence",
    "Strategic developments"
]

# Determine week - previous full Monday–Sunday
today = datetime.utcnow()
start = today - timedelta(days=today.weekday() + 7)  # last Monday
end = start + timedelta(days=6)                     # last Sunday

# load and filter
df = pd.read_csv(input_file, low_memory=False, encoding="utf-8")

# fix datetime formt
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
df = df.dropna(subset=['event_date'])

# apply filters
mask = (
    (df['event_date'] >= start) &
    (df['event_date'] <= end) &
    (df['country'] == "United States") &
    (df['event_type'].isin(tension_event_types))
)
df_filtered = df[mask]

# aggregate to weekly avg
total_events = len(df_filtered)

# === Save summary ===
summary_df = pd.DataFrame([{
    'WEEK_START': start.strftime('%Y-%m-%d'),
    'WEEK_END': end.strftime('%Y-%m-%d'),
    'TOTAL_EVENTS': total_events,
    'KEY_RISK_INDICATOR_ID': kri_id
}])

os.makedirs(output_dir, exist_ok=True)
if os.path.isfile(output_file):
    summary_df.to_csv(output_file, mode='a', index=False, header=False)
else:
    summary_df.to_csv(output_file, index=False)

print(f"Saved weekly ACLED tension summary to {output_file}")
