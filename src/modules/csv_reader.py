import pandas as pd

'''
file pathで指定したcsvからデータを取得してdfを返す
'''

def read_csv_and_import_pdr(csv_file_path):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path, usecols=['flag', 'date', 'symbol', 'action', 'price', \
                                                'stop', 'unit', 'win_lose', 'appendix'])
    return df


def main():
    csv_file_path = 'csv/imai.csv'
    data_frame = read_csv_and_import_pdr(csv_file_path)
    print(data_frame.head())



if __name__ == '__main__':
    main()
