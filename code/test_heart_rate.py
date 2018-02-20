def test_import():
    from heart_rate import ECG
    first_set = ECG(filename="test_data1.csv")

    assert first_set.time[0] == 0
    assert first_set.time[-1] == 27.775
    assert first_set.voltage[0] == -0.145
    assert first_set.voltage[-1] == 0.72

    second_set = ECG(filename="test_data27.csv")
    assert second_set.time[0] == 0
    assert second_set.time[-1] == 39.996
    assert second_set.voltage[0] == -0.175
    assert second_set.voltage[-1] == -1.7725


def test_attributes():
    pass


def test_export():
    pass
