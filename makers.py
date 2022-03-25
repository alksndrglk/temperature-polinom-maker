from scipy.linalg import lstsq
from svet_template import template
from multiprocessing import JoinableQueue
import pandas as pd
import json
import numpy as np

from config import Params, columns


def make_koefficients(params: Params):
    result = []
    M_size = [i for i in range(params.degree + 1)]
    if params.breakpoint:
        left, right = (0, params.breakpoint + 1), (
            params.breakpoint - 1,
            len(params.temperature),
        )
        start, finish = (
            params.temperature.iloc[0],
            params.temperature.iloc[params.breakpoint - 1],
        )
    else:
        left, right = (0, len(params.temperature)), (0, 0)
        start, finish = params.temperature.iloc[0], params.temperature.iloc[-1]
    for part in (left, right):
        M = params.temperature.to_numpy()[part[0] : part[1], np.newaxis] ** M_size
        p, *_ = lstsq(M, params.target.to_numpy()[part[0] : part[1]])
        x = np.linspace(start, finish, 300)
        y = sum([p[i] * x ** i for i in range(params.degree + 1)])
        result.append({'line': make_line(p), 'x': x, 'y': y})
        if right == (0, 0):
            break
        start, finish = (
            params.temperature.iloc[params.breakpoint - 1],
            params.temperature.iloc[-1],
        )
    return result


def make_settings_queue(
    breakpoint: int,
    nach: pd.DataFrame,
    kon: pd.DataFrame,
) -> JoinableQueue:

    worker_settings = JoinableQueue()
    for i in columns[1:]:
        polynomial_degree = 3
        if i.startswith("fW"):
            polynomial_degree = 1
        worker_settings.put(
            Params(
                name=i,
                target=nach[i],
                temperature=nach["p2"],
                degree=polynomial_degree,
                breakpoint=breakpoint,
            )
        )
        worker_settings.put(
            Params(
                name=i,
                target=kon[i],
                temperature=kon["p2"],
                degree=polynomial_degree,
                breakpoint=breakpoint,
            )
        )
    return worker_settings


def make_line(koefs: np.ndarray):
    # degree_list = ["*P2" * i for i in range(0, len(koefs) + 1)]
    degree_list = ["", "*P2", "*P2_sq", "*P2_cube"]
    return "".join(f"{a:+f}{b}" for a, b in zip(koefs, degree_list[: len(koefs)]))


def unpack(s):
    return "".join(map(str, s))


def make_dos_C_file(path, data):
    temp_kalibr_text = "\n".join(f"{k} = {v};" for (k, v) in data.items())

    with open(path + "SVET.C", "w") as f:
        f.write(template.format(temperature_correction=temp_kalibr_text))


def make_txt_from_json(path, data) -> None:
    with open(path + "all_koef.txt", "w") as f:
        json.dump(data, f, indent=4)
