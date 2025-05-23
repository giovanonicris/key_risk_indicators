import pandas as pd

# get 10y-2y treasury yield spread from fred
def get_fred_yield_curve_spread():
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y'
    df = pd.read_csv(url, parse_dates=['DATE'])
    df = df.dropna().sort_values('DATE', ascending=False)
    print(df[['DATE', 'T10Y2Y']].head(5))

if __name__ == '__main__':
    get_fred_yield_curve_spread()