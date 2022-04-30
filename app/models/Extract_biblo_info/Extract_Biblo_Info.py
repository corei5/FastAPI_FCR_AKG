# Parse HTML table and import to Pandas DataFrame
import pandas as pd
import json
from fastapi import FastAPI, HTTPException, Request, status


def extract_biblo_info(full_url):
    df_list = []
    try:
        table_MN = pd.read_html(full_url, attrs={'class': 'description'})
        print(f'Total tables: {len(table_MN)}')
        df_table = table_MN[0]
        df_list.append(df_table)
        result = df_table.to_json(orient="index")
        parsed = json.loads(result)
        return_json = json.dumps(parsed, indent=4)
        return return_json

    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Not able to extract biblo info")


