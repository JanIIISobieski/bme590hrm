def test_import():
    from heart_rate import ECG
    first_set = ECG(filename='test_data1.csv')

    assert first_set.time[0] == 0
    assert first_set.time[-1] == 27.775
    assert first_set.voltage[0] == -0.145
    assert first_set.voltage[-1] == 0.72

    second_set = ECG(filename='test_data27.csv')
    assert second_set.time[0] == 0
    assert second_set.time[-1] == 39.996
    assert second_set.voltage[0] == -0.175
    assert second_set.voltage[-1] == -1.7725


def test_attributes():
    from heart_rate import ECG
    first_set = ECG(filename='test_data8.csv')
    assert first_set.voltage_extremes == (-3.105, 1.975)
    assert first_set.duration == 27.775

    second_set = ECG(filename='test_data18.csv')
    assert second_set.voltage_extremes == (-0.19375, 0.7875)
    assert second_set.duration == 13.887


def test_beat_finding():
    import glob
    import os
    from heart_rate import ECG
    csv_loc = os.path.join(os.path.dirname(__file__), '../test_data/*.csv')
    num_beats_actual = [35, 19, 19, 32, 19, 19, 37, 74, 79, 29, 36, 44, 63, 35,
                        10, 34, 78, 19, 19, 33, 35, 37, 33, 32, 33, 28, 9, 4,
                        7, 7, 19, 19]
    num_beats_found = []
    for csv_file in glob.glob(csv_loc):
        test = ECG(filename=os.path.basename(csv_file), export=True)
        num_beats_found.append(len(test.beats))

    tot_beats_actual = sum(num_beats_actual)
    tot_beats_found = sum(num_beats_found)

    assert abs((tot_beats_actual - tot_beats_found)/(tot_beats_actual)) < 0.01


def test_heart_rate():
    from heart_rate import ECG
    first_set = ECG(filename='test_data20.csv')
    assert abs(int(first_set.mean_hr_bpm) - 81)/81 < 0.05


def test_export():
    from heart_rate import ECG
    import os
    import json
    import numpy as np

    test = ECG()
    json_loc = os.path.join(os.path.dirname(__file__),
                            '../JSON/test_data1.json')
    with open(json_loc, 'r') as fp:
        json_import = json.load(fp)

    assert np.allclose(test.voltage, json_import['voltage'])
