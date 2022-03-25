import argparse
import pathlib
import pandas as pd
from config import columns

class FileSplitter:
    def __init__(self, args: argparse.Namespace):
        self._path = args.path
        self._interval = args.interval
        self._shift = args.shift

    def __call__(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        try:
            file_path = sorted(pathlib.Path(self._path).glob("MASS*.csv"))[0]
        except IndexError:
            print("Файла MASS*.csv нет в этой дирректории")
            exit()
        df = pd.read_csv(file_path, sep=";", decimal=",", names=columns, skiprows=1)
        nach = []
        kon = []
        min_end_value = 1
        for i in range(0, len(df), self._interval):
            if i:
                min_end_value = df["p2"].iloc[i - self._shift]
                kon.append(df.iloc[i - self._shift])
            nach.append(
                df.iloc[
                    next(
                        j for j in range(i, len(df)) if df["p2"].iloc[j] < min_end_value
                    )
                ]
            )
        kon.append(df.loc[len(df) - 1])

        return (pd.DataFrame(kon), pd.DataFrame(nach))
