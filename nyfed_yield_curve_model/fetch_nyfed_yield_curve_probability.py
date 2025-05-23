import pandas as pd

# get ny fed yield curve recession probability
def get_nyfed_yield_curve_prob():
    url = 'https://www.newyorkfed.org/medialibrary/media/research/capital_markets/Prob_Rec.csv'
    df = pd.read_csv(url, skiprows=4)
    df = df.rename(columns=lambda x: x.strip())
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    latest = df.dropna().sort_values('DATE', ascending=False).head(1)
    print(latest[['DATE', 'P(REC)']])

if __name__ == '__main__':
    get_nyfed_yield_curve_prob()