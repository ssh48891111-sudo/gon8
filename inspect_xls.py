import pandas as pd
import glob
import os

try:
    files = glob.glob('논문*.xls')
    print("Files found:", files)
    
    # KCI에서 다운로드한 .xls는 종종 실제로는 HTML 테이블인 경우가 있습니다.
    # 일단 read_html 로 시도하고, 안되면 read_excel 로 시도합니다.
    df_list = []
    for f in files:
        try:
            dfs = pd.read_html(f, encoding='utf-8')
            if dfs:
                df_list.append(dfs[0])
                print(f"{f} loaded as HTML, shape: {dfs[0].shape}")
        except Exception as e:
            # HTML이 아닌 실제 엑셀일 경우
            df = pd.read_excel(f)
            df_list.append(df)
            print(f"{f} loaded as Excel, shape: {df.shape}")
            
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        print("Combined shape:", combined_df.shape)
        print("Columns:", combined_df.columns.tolist())
except Exception as e:
    print("Error:", e)
