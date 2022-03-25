#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt

from splitter import FileSplitter
from worker import Worker
from makers import make_settings_queue, make_txt_from_json, make_dos_C_file


def main():
    parser = argparse.ArgumentParser(
        "Получим из файла MASSIV.csv коэффициенты температурной калибровки."
    )
    parser.add_argument(
        "-i",
        "--interval",
        required=True,
        type=int,
        help="Интервал измерений в зависимости от заявленной точности",
    )
    parser.add_argument(
        "-s",
        "--shift",
        type=int,
        default=0,
        help="Сдвиг конечного измерения в зависимости от точности.",
    )
    parser.add_argument(
        "-g",
        "--graph",
        action="store_true",
        default=False,
        help="Флаг для построения графика",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="./",
        help="Путь до дирректории с файлом MASSIV.csv",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store_true",
        default=False,
        help="Создать файл SVET с полученными коэффициентами",
    )
    parser.add_argument(
        "-b",
        "--breakpoint",
        type=int,
        default=0,
        help="Сдвиг конечного измерения в зависимости от точности.",
    )
    args = parser.parse_args()

    kon, nach = FileSplitter(args)()

    worker_settings = make_settings_queue(args.breakpoint, nach, kon)
    data = Worker(worker_settings)()
    make_txt_from_json(args.path, data)

    if args.file:
        make_dos_C_file(args.path, data)

    if args.graph:
        plt.show()


if __name__ == "__main__":
    main()
