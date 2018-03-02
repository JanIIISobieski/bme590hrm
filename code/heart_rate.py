class ECG:
    def __init__(self, filename='test_data1.csv', units='sec'):
        self.filename = filename
        self.units = units
        self.import_csv()
        self.find_volt_extrema()
        self.find_duration()
        self.find_beats()
        self.find_mean_hr_bpm()
        pass

    def import_csv(self):
        import pandas
        import logging
        import os
        import numpy as np
        full_file = os.path.join(os.path.dirname(__file__), '../test_data/',
                                 self.filename)
        imported_file = pandas.read_csv(full_file,
                                        header=None,
                                        names=['time', 'voltage'],
                                        skipinitialspace=True)

        time_vec = imported_file.time.values
        voltage_vec = imported_file.voltage.values

        bad_vals = []
        if isinstance(time_vec[0], str):
            for n, i in enumerate(time_vec):
                try:
                    float(i)
                except ValueError:
                    bad_vals.append(n)

            for n, i in enumerate(voltage_vec):
                try:
                    float(i)
                except ValueError:
                    bad_vals.append(n)

        time_vec = np.delete(time_vec, bad_vals)
        voltage_vec = np.delete(voltage_vec, bad_vals)

        time_vec = np.ndarray.astype(time_vec, float)
        voltage_vec = np.ndarray.astype(voltage_vec, float)

        nan_index_time = np.argwhere(np.isnan(time_vec))
        nan_index_voltage = np.argwhere(np.isnan(voltage_vec))
        all_nans = np.vstack((nan_index_time, nan_index_voltage))

        if all_nans.size != 0:
            self.time = np.delete(time_vec, all_nans)
            self.voltage = np.delete(voltage_vec, all_nans)
            logging.warning('Removed NaN rows from the array')
        else:
            self.time = time_vec
            self.voltage = voltage_vec

        logging.info('Successfully imported CSV file')

    def find_mean_hr_bpm(self, time_dur=60):
        beat_times = self.beats

        if time_dur >= self.duration:
            self.mean_hr_bpm = 60*len(beat_times)/self.duration
        else:
            beat_num = len([i for i in beat_times if beat_times <= time_dur])
            self.mean_hr_bpm = 60*beat_num/time_dur
        print(self.mean_hr_bpm)

    def find_volt_extrema(self):
        from numpy import amin, amax
        self.voltage_extremes = (amin(self.voltage), amax(self.voltage))

    def find_duration(self):
        import logging
        if self.units == 'sec':
            net_dur = self.time[-1] - self.time[0]
        elif self.units == 'min':
            net_dur = (self.time[-1] - self.time[0])*60
        elif self.units == 'msec':
            print('This program is not for hummingbirds')
            net_dur = self.time[-1] - self.time[0]
        else:
            net_dur = self.duration
            print('Assuming seconds for time')
            logging.warning('Assuming seconds for time')
        self.duration = net_dur

    def find_num_beats(self):
        self.num_beats = len(self.beats)

    def find_beats(self, show_plot=True):
        import numpy as np
        import logging
        from math import floor
        from detect_peaks import detect_peaks

        voltage = self.voltage
        time = self.time

        try:
            baseline_coeffs = np.polyfit(time, voltage, 7)
            voltage = voltage - np.polyval(baseline_coeffs, time)
        except np.linalg.LinAlgError:
            print('Could not remove baseline drift (if it exists)')
            logging.warning('Could not remove baseline drift')

        unbias = voltage - np.mean(voltage)
        norm = sum(unbias**2)
        auto_corr = np.correlate(unbias, unbias, mode="full")/norm
        auto_corr = auto_corr[floor(len(auto_corr)/2):]

        pre_peak_index = detect_peaks(auto_corr, mpd=5, mph=0)
        sorted_auto_corr = sorted(auto_corr[pre_peak_index])

        beat_ind = np.asarray([0])
        index = -1
        while (beat_ind.size/self.duration < 0.3):
            first_dist = np.where(auto_corr == sorted_auto_corr[index])[0][0]
            beat_ind = detect_peaks(np.insert(auto_corr, 0, 0),
                                    mpd=0.8*first_dist,
                                    mph=0)
            beat_ind = beat_ind - 1
            index = index - 1
            print(beat_ind.size)
            print(index)

        self.auto_corr = auto_corr
        self.beat_index = beat_ind
        self.beats = self.time[beat_ind]

    def export_json():
        pass
