import pandas as pd


def extract_and_save_to_csv(tipster_dataframes, PERSON):
    """
    リストに入ったデータフレームから指定された情報を抽出し、新しいデータフレームを作成してCSVファイルに出力する関数。

    :param tipster_dataframes: データフレームのリスト
    :param output_csv: 出力するCSVファイルのパス
    """

    # csvを新規作成
    with open(f'data/csv/{PERSON}.csv', 'w') as f:
        f.close

    # データフレーム処理
    records = []
    for df in tipster_dataframes:
        # 日付をDatetime型に変換
        df['date'] = pd.to_datetime(df['date'])

        # openの日付とcloseの日付を取得して文字列に変換
        open_date = df[df['flag'] == 'open']['date'].iloc[0].strftime('%Y-%m-%d %H:%M')
        close_date = (df[df['flag'] == 'close']['date'].iloc[0]).strftime('%Y-%m-%d %H:%M')

        # symbolを取得
        df_symbol = df['symbol'].iloc[0]

        # actionを取得
        df_action = df[df['flag'] == 'open']['action'].iloc[0]

        # 平均取得価格を計算
        df_action = df[df['flag'] != 'close']
        mean_price = df_action['price'].mean()

        # unitを取得
        df_unit = df['unit'].sum()

        # 勝敗を取得
        square_price = str(df[df['flag'] == 'close']['price'].iloc[0])
        if df_action == "long":
            if mean_price < square_price:
                result = "win"
            else:
                result = "lose"
        elif df_action == "short":
            if mean_price > square_price:
                result = "win"
            else:
                result = "lose"
        df_win_lose = result

        # レコードを作成
        record = {
            'open': open_date,
            'close': close_date,
            'symbol': df_symbol,
            'action': df_action,
            'average_price': mean_price,
            'square_price': square_price,
            'unit': df_unit,
            'win_lose': df_win_lose
        }
        records.append(record)

    # 新しいデータフレームを作成
    result_df = pd.DataFrame(records, columns=['open', 'close', 'symbol', 'action', 'average_price', 'square_price', 'unit', 'win_lose'])

    # CSVファイルに出力
    result_df.to_csv(f'data/csv/{PERSON}.csv', index=False)