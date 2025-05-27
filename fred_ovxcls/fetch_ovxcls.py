from fredapi import Fred
import pandas as pd
import os

fred = Fred(api_key=os.environ['FRED_API_KEY'])
ovx_data = fred.get_series('OVXCLS')
ovx_df = ovx_data.reset_index()
ovx_df.columns = ['date', 'ovxcls']
ovx_df.to_csv('ovxcls.csv', index=False)
print("Updated ovxcls.csv")