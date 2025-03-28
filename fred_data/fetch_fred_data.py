import os
import pandas as pd
from fredapi import Fred

# load FRED key
fred_api_key = os.getenv("FRED_API_KEY")
if not fred_api_key:
    raise ValueError("Problem with FRED_API_KEY.")

fred = Fred(api_key=fred_api_key)

# load kri mapping
kri_df = pd.read_csv("fred_data/kri_list.csv")
name_to_id = dict(zip(kri_df["KEY_RISK_INDICATOR"], kri_df["KEY_RISK_INDICATOR_ID"]))

# define Start Date
start_date = "2020-01-01"

# define series and names
data_series = {
    "Labor": {
        "series": ["UNRATE", "UNEMPLOY", "JTSJOL", "JTSQUL", "JTU5100JOL",
                   "JTU5200JOL", "JTS540099JOL", "JTU5100QUL", "JTU5200QUL", 
                   "JTS540099QUL", "LNU04032237", "LNU04032238", "LNU04032239", 
                   "FRBATLWGT12MMUMHGO", "FRBATLWGT12MMUMHWGJST", "FRBATLWGT12MMUMHWGJSW"],
        "names": ["US Unemployment Rate", "US Unemployment Level", "US Job Openings", 
                  "US Voluntary Separations (Quits)", "US Job Openings (Information)", 
                  "US Job Openings (Finance and Insurance)", "US Job Openings (Professional and Business Services)", 
                  "Quits (Information)", "Quits (Finance and Insurance)", "Quits (Professional and Business Services)", 
                  "Unemployment Rate (Information)", "Unemployment Rate (Finance and Insurance)", 
                  "Unemployment Rate (Professional and Business Services)", 
                  "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Overall)",
                  "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Stayer)",
                  "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Switcher)"]
    },
    "Treasury": {
        "series": ["DGS10"],
        "names": ["10-Year Treasury Yields"]
    },
    "Risk": {
        "series": ["BAMLHYH0A0HYM2TRIV", "VIXCLS", "STLFSI4", "NFCI"],
        "names": ["ICE BofA US High Yield Index Total Return Index Value", "CBOE Volatility Index VIX",
                  "St Louis Fed Financial Stress Index", "Chicago Fed National Financial Conditions Index"]
    },
    "Econ": {
        "series": ["FEDFUNDS", "T10Y2Y", "MORTGAGE30US", "CPALTT01USM657N", "PPIACO", "A191RL1Q225SBEA"],
        "names": ["Federal Funds Effective Rate", 
                  "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity", 
                  "30-Year Fixed Rate Mortgage Average in the United States", 
                  "Consumer Price Index: All Items: Total for United States",
                  "Producer Price Index by Commodity: All Commodities", 
                  "Real Gross Domestic Product"]
    }
}

# fetch FRED data
df_new = pd.DataFrame()
for category, details in data_series.items():
    for series, name in zip(details["series"], details["names"]):
        kri_id = name_to_id.get(name)
        if kri_id is None:
            continue  # skip if no ID match
        temp_data = fred.get_series(series, observation_start=start_date)
        temp_data = temp_data.to_frame(name=kri_id)  # use KRI ID as column name
        df_new = pd.merge(df_new, temp_data, left_index=True, right_index=True, how="outer")
        
df_new.reset_index(inplace=True)
df_new.rename(columns={"index": "Date"}, inplace=True)

# apply data transformations
multipliers = {
    "US Unemployment Level": 1000, "US Job Openings": 1000, "US Voluntary Separations (Quits)": 1000,
    "US Job Openings (Information)": 1000, "US Job Openings (Finance and Insurance)": 1000,
    "US Job Openings (Professional and Business Services)": 1000, "Quits (Information)": 1000,
    "Quits (Finance and Insurance)": 1000, "Quits (Professional and Business Services)": 1000
}

percentages = [
    "US Unemployment Rate", "Unemployment Rate (Information)", "Unemployment Rate (Finance and Insurance)",
    "Unemployment Rate (Professional and Business Services)", 
    "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Overall)",
    "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Stayer)",
    "12-Month Moving Average of Unweighted Median Hourly Wage Growth (Switcher)",
    "10-Year Treasury Yields"
]

# convert using IDs
for name, multiplier in multipliers.items():
    col_id = name_to_id.get(name)
    if col_id and col_id in df_new.columns:
        df_new[col_id] *= multiplier

for name in percentages:
    col_id = name_to_id.get(name)
    if col_id and col_id in df_new.columns:
        df_new[col_id] /= 100

# generate wide form
csv_path = "fred_data/fred_data.csv"
if os.path.exists(csv_path):
    df_old = pd.read_csv(csv_path, parse_dates=["Date"])
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset=["Date"], keep="last", inplace=True)
else:
    df_combined = df_new

# unpivot to long-form
df_long = df_combined.melt(id_vars="Date", var_name="KEY_RISK_INDICATOR_ID", value_name="Value")
df_long["KEY_RISK_INDICATOR_ID"] = df_long["KEY_RISK_INDICATOR_ID"].astype(int)

# write to file
df_long.to_csv("fred_data/fred_normalized.csv", index=False)
