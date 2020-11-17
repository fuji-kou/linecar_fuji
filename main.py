import numpy as np
import csv

import linecar_settings as sets
from models.LineCar import LineCar
from controllers.FujitaControl import FujitaControl
from controllers.PurePursuitControl import PurePursuitControl


def main():
    record = []

    m1 = LineCar()
    m1.setup4experiment()
    m1.controller.prepare()
    # 発進
    m1.mv_wheel(sets.SPEED)
    # 操作ループ
    while(True):
        try:
            now_latlon = m1.get_current_position()
            input_angle = m1.controller.get_input_angle()
            m1.mv_angle(round(input_angle, 1))
            record.append(m1.get_status())
            if m1.controller.is_finished():
                m1.mv_wheel(0)
                break
        except KeyboardInterrupt:
            m1.stop()
    # 終了処理
    m1.stop()

    with open('./output.csv', 'w') as csv_out:
        writer = csv.writer(csv_out, lineterminator='\n')
        writer.writerows(record)


if __name__ == '__main__':
    main()
