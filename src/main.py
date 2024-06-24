from modules import csv_reader
from modules import extraction_df
from modules import plot
from modules import output_csv


# 読み込みたいcsvを指定してください
PERSON = "imai"


def main():

    # csvを読み込む
    df = csv_reader.read_csv_and_import_pdr(f"csv/{PERSON}.csv")

    # 対象のデータフレームを取り出す
    extracted_dfs = extraction_df.get_individual_periods(df)

    # プロットする
    plot.plot_tipster_result(extracted_dfs, PERSON)

    # cscに結果を残す
    #output_csv.extract_and_save_to_csv(extracted_dfs, PERSON)

    print()
    print()
    print('--- プログラムを終了します ---')


if __name__ == '__main__':
    main()