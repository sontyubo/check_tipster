from datetime import timedelta

import pandas as pd
from pandas_datareader import data as pdr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import japanize_matplotlib

import yfinance as yfin


SYMBOL = {
    "ドル円": "USDJPY=X",
    "ポンド円": "GBPJPY=X",
    "ユーロ円": "EURJPY=X",
    "ユーロドル": "EURUSD=X",
}

def get_hour_market_dataframe(symbol, start_date, end_date):
    """
    指定された「通貨」「期間」の1時間足をYahooファイナンスから取得する関数
    """
    yfin.pdr_override()
    df = pdr.get_data_yahoo(symbol, start=start_date, end=end_date, interval="1h")
    df = df.reset_index()
    return df


def plot_tipster_result(tipster_dataframes:list, PERSON:str):
    """
    リスト内の複数のデータフレームをプロットする関数
    """

    for i, df in enumerate(tipster_dataframes):
        plt.figure(figsize=(10, 6))
        
        # 日付をDatetime型に変換
        df['date'] = pd.to_datetime(df['date'])

        # 開始と終了の日付を取得
        open_date = df[df['flag'] == 'open']['date'].iloc[0].strftime('%Y-%m-%d')
        close_date = df[df['flag'] == 'close']['date'].iloc[0] + timedelta(days=1)
        close_date = close_date.strftime('%Y-%m-%d')

        # 通貨を取得
        df_symbol = df['symbol'].iloc[0]

        # actionを取得
        df_action = str(df[df['flag'] == 'open']['action'].iloc[0])

        # マーケットデータ取得
        assert df_symbol in SYMBOL.keys(), "yahooファイナンスを呼び出す通貨エラー"
        market_df = get_hour_market_dataframe(SYMBOL[df_symbol], open_date, close_date)

        
        # date列をx軸、price列をy軸にプロット
        ## マーケットデータ
        plt.plot(market_df["Datetime"], market_df["Close"], marker='.', label="Close Price", color="blue")

        ## Tipsterデータ
        ### 開始ポイント
        open_point = df[df['flag'] != 'close']
        plt.scatter(open_point['date'], open_point['price'], marker='o', color='red', label='Action Point')
        ### 終了ポイント
        end_point = df[df['flag'] == 'close']
        plt.scatter(end_point['date'], end_point['price'], marker='s', color='green', label='Square Point')
        

        # グラフのタイトルとラベルを設定
        plt.title(f'{open_date}_{close_date}_{df_symbol}_{df_action}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid()
        plt.legend()

        # x軸のラベルを補助目盛を1hごと、メジャー目盛を12時間ごとに設定
        ax = plt.gca()
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        
        # グラフを表示
        #plt.show()

        # グラフの保存
        plt.savefig(f"data/plot/{PERSON}/{open_date}_{close_date}_{df_symbol}_{df_action}.png")