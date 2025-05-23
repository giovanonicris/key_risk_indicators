import pandas as pd
import requests
import zipfile
import io
from datetime import datetime, timedelta
import os

kri_id = 104
TENSION_THEMES = ['PROTEST', 'MILITARY', 'SANCTIONS', 'TRADE_WAR', 'DIPLOMACY']

def get_latest_gkg_file_url():
    now = datetime.utcnow()
    for days_back in [0, 1]:
        day = now - timedelta(days=days_back)
        base_url = f"http://data.gdeltproject.org/gdeltv2/{day.strftime('%Y%m%d')}"
        for hour in range(23, -1, -1):
            hour_str = f"{hour:02}0000"
            url = f"{base_url}{hour_str}.gkg.csv.zip"
            r = requests.head(url)
            if r.status_code == 200:
                return url, day.strftime('%Y-%m-%d'), hour
    return None, None, None

def download_and_process_gkg(url, date_label, hour):
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    filename = z.namelist()[0]
    with z.open(filename) as f:
        df = pd.read_csv(f, sep='\t', header=None, quoting=3, low_memory=False)
    # assign col names as per GDELT GKG v2 spec (reduced set)
    df.columns = ['GKGRECORDID', 'DATE', 'SourceCollectionIdentifier', 'SourceCommonName',
                  'DocumentIdentifier', 'V2THEMES', 'V2ENHANCEDTHEMES', 'V2ENHANCEDPERSONS',
                  'V2ENHANCEDORGS', 'V2ENHANCEDCOUNTRIES', 'V2ENHANCEDADM1', 'V2ENHANCEDADM2',
                  'V2ENHANCEDLOCATIONS', 'V2ENHANCEDWEAPONS', 'V2GCAM', 'V2CLUSTERCountries',
                  'V2Counts', 'V2EnhancedCounts', 'V2Themes', 'V2Locations', 'V2Persons',
                  'V2Organizations', 'V2Tone', 'V2EnhancedThemes2'
                 ][:len(df.columns)]
    is_us = df['V2ENHANCEDCOUNTRIES'].astype(str).str.contains('USA', na=False)
    is_tension = df['V2THEMES'].astype(str).apply(lambda x: any(theme in x for theme in TENSION_THEMES))
    df_filtered = df[is_us & is_tension]
    df_filtered['TONE_VAL'] = df_filtered['V2Tone'].astype(str).str.split(',').str[0].astype(float)
    avg_tone = df_filtered['TONE_VAL'].mean() if not df_filtered.empty else None
    count = len(df_filtered)
    result_df = pd.DataFrame([{
        'DATE': date_label,
        'HOUR': hour,
        'AVG_TONE': avg_tone,
        'ARTICLE_COUNT': count,
        'KEY_RISK_INDICATOR_ID': kri_id
    }])
    return result_df

def main():
    url, date_label, hour = get_latest_gkg_file_url()
    output_file = 'gdelt_geopolitical_tensions/gdelt_us_geopolitical_tension.csv'
    os.makedirs('gdelt_us_tension', exist_ok=True)
    if url:
        result_df = download_and_process_gkg(url, date_label, hour)
        # append or write header if file doesn't exist
        if os.path.isfile(output_file):
            result_df.to_csv(output_file, mode='a', index=False, header=False)
        else:
            result_df.to_csv(output_file, index=False)
        print(f"GDELT tension data saved to {output_file}")
    else:
        print("No recent GDELT GKG file found.")

if __name__ == "__main__":
    main()