class ECG:
    def __init__(self, filename='test_data1.csv'):
        self.filename = filename
        self.import_csv()
        self.find_volt_extrema()
        self.find_duration()
        self.find_beats()
        pass

    def import_csv(self):
        import pandas
        import logging
        import os
        full_file = os.path.join(os.path.dirname(__file__), '../test_data/',
                                 self.filename)
        imported_file = pandas.read_csv(full_file,
                                        header=None,
                                        names=['time', 'voltage'],
                                        skipinitialspace=True)
        self.time = imported_file.time.values
        self.voltage = imported_file.voltage.values
        logging.info('Successfully imported CSV file')

    def find_mean_hr_bpm(self, time_dur=1):
        pass

    def find_volt_extrema(self):
        from numpy import amin, amax
        self.voltage_extremes = (amin(self.voltage), amax(self.voltage))

    def find_duration(self):
        self.duration = self.time[-1] - self.time[0]

    def find_num_beats(self):
        self.num_beats = len(self.beats)

    def find_beats(self, show_plot=True):
        import matplotlib.pyplot as plt
        from numpy import polyfit, polyval, mean, sum, correlate, where, insert
        from math import floor
        from detect_peaks import detect_peaks
        baseline_coeffs = polyfit(self.time, self.voltage, 7)
        detrend = self.voltage - polyval(baseline_coeffs, self.time)
        unbias = detrend - mean(detrend)
        norm = sum(unbias**2)
        auto_corr = correlate(unbias, unbias, mode="full")/norm
        auto_corr = auto_corr[floor(len(auto_corr)/2):]

        pre_peak_index = detect_peaks(auto_corr, mpd=5, mph=0)
        sorted_auto_corr = sorted(auto_corr[pre_peak_index])

        first_dist = where(auto_corr == sorted_auto_corr[-1])[0][0]
        beat_ind = detect_peaks(insert(auto_corr, 0, 0),
                                mpd=0.8*first_dist,
                                mph=0)
        beat_ind = beat_ind - 1

        self.auto_corr = auto_corr
        self.beat_index = beat_ind

    def export_json():
        pass
