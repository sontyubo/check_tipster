import pandas as pd

'''
example

2   NaN  2024-05-09 15:28:00    NaN    NaN     NaN   NaN   NaN      NaN      NaN
3   NaN   2024-05-07 8:16:00    NaN    NaN     NaN   NaN   NaN      NaN      NaN
4  open   2024-05-07 8:13:00    ドル円   long  154.02   NaN   2.0      NaN      NaN
'''

def get_individual_periods(df):
    # 'flag' が 'open' から 'close' までの期間のデータフレームを個別に取り出す
    data_frame_periods = []
    current_period = None

    # データフレームを下から順に入れ替える
    df = df.iloc[::-1]

    for index, row in df.iterrows():
        if row['flag'] == 'open':
            current_period = [row]
        elif row['flag'] == 'close' and current_period is not None:
            current_period.append(row)
            data_frame_periods.append(pd.DataFrame(current_period))
            current_period = None
            #yield data_frame_periods
        elif current_period is not None:
            current_period.append(row)
    
    return data_frame_periods
