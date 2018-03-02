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


def test_export():
    pass
