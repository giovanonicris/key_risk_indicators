import pandas as pd

# get vix closing values from fred
def get_fred_vix():
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'
    df = pd.read_csv(url, parse_dates=['DATE'])
    df = df.dropna().sort_values('DATE', ascending=False)
    print(df[['DATE', 'VIXCLS']].head(5))

if __name__ == '__main__':
    get_fred_vix()