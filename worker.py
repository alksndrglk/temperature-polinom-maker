from dataclasses import dataclass
from multiprocessing import Pool, JoinableQueue
from queue import Empty

from makers import make_koefficients, unpack


@dataclass
class Worker:
    settings: JoinableQueue

    def __call__(self):

        koefs_data = {}
        with Pool(processes=10) as pool:
            while True:
                try:
                    n_settings = self.settings.get_nowait()
                    k_settings = self.settings.get_nowait()
                    _nach = pool.apply_async(make_koefficients, (n_settings,))
                    _kon = pool.apply_async(make_koefficients, (k_settings,))

                    _nach = _nach.get()[0]
                    _kon = _kon.get()[0]
                    data = {
                        f"{n_settings.name}na": unpack(_nach.get('line')),
                        f"{k_settings.name}kon": unpack(_kon.get('line')),
                    }
                    koefs_data.update(data)
                except Empty:
                    print("Коэффициенты рассчитаны для всех столбцов")
                    break

        return koefs_data
