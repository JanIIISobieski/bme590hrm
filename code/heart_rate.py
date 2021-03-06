class ECG:
    '''Class to describe ECG trace data. Utilizes detect_peaks written by
    Marcos Duarte and made available with the MIT license for the detection of
    peaks in the auto-correlated signal

    :attribute filename (str): CSV filename from which data was imported
    :attribute time (array): sampled times of the ECG trace
    :attribute voltage (array): sampled voltages of the ECG trace
    :attribute voltage_extremes (tuple): minimum and maximum sampled voltage
    :attribute duration (float): total time of ECG sampling
    :attribute beats (array): array of times when heartbeat was detected
    :attribute num_beats (int): number of heart beats detected in ECG trace
    :attribute mean_hr_bpm (float): average heart rate over a user-specified
        time interval
    '''
    def __init__(self, filename='test_data1.csv', units='sec', export=False):
        '''__init__ method of the ECG class

        :param filename (str, default='test_data1.csv'): CSV file containing
            ECG trace data. Filename should include the .csv extension.
            File by default should be in a 'test_data' folder one level higher
            than where the module resides
        :param units (str, default='sec'): defines the time scale of the data.
            By default set to 'sec' for seconds. 'Min' can also be passed.
        :param export (boolean, default=False): exports JSON file based on
            analysis
        '''
        import logging

        logging.basicConfig(filename="heart_rate.log",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        self.filename = filename
        self.__run_flag = True
        self.units = units
        self.import_csv()  # can manipulate __run_flag if import file not found
        if self.__run_flag:
            self.find_volt_extrema()
            self.find_duration()
            self.find_beats()
            self.find_num_beats()
            self.find_mean_hr_bpm()

            if export:
                self.export_json()

    def import_csv(self):
        '''Class method to import CSV

        :return time (numpy array): array of the sampled times in ECG trace
        :return voltage (numpy array): array of the sampled voltages in ECG
            trace
        '''
        import pandas
        import logging
        import os
        import numpy as np

        try:
            full_file = os.path.join(os.path.dirname(__file__),
                                     '../test_data/',
                                     self.filename)
            imported_file = pandas.read_csv(full_file,
                                            header=None,
                                            names=['time', 'voltage'],
                                            skipinitialspace=True)
        except FileNotFoundError:
            logging.error('Import file not found!')
            logging.info('Terminating execution')
            self.__run_flag = False
            return

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
        '''Class method to find the mean heart rate during the first specified
            interval in data

            :param time_dur (default=60): in seconds, the interval (starting
                from 0 seconds) over which to count beats to calculate the
                average spike rate. If time_dur is greater than the total
                duration of the data set, the average heart rate over the
                entire data set is given
            :return mean_hr_bpm (float): the mean heart rate over the interval
        '''
        beat_times = self.beats

        if time_dur >= self.duration:
            self.mean_hr_bpm = 60*len(beat_times)/self.duration
        else:
            beat_num = len([i for i in beat_times if beat_times <= time_dur])
            self.mean_hr_bpm = 60*beat_num/time_dur

    def find_volt_extrema(self):
        '''Class method to find the voltage extremes in ECG trace

        :return voltage_extremes (tuple): the minimum and maximum voltage
            values sampled
        '''
        from numpy import amin, amax
        import logging
        self.voltage_extremes = (amin(self.voltage), amax(self.voltage))
        ecg_range = 300
        if (self.voltage_extremes[1] - self.voltage_extremes[0]) > ecg_range:
            logging.warning('Data set exceeds ECG specifications')

    def find_duration(self):
        '''Class method to find the duration of ECG trace in seconds

        :return duration (float): the total time of the sampled ECG
        '''
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
        '''Class method to find the total number of beats in the data set

            :return num_beats (int): the number of beats found by the program
        '''
        self.num_beats = len(self.beats)

    def find_beats(self):
        '''Class method to find the heart beats during the data set

        :return beats (list): the times at which a heart beat was found
        '''
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

        self.beats = self.time[beat_ind]

    def export_json(self):
        '''Class method to export the class attributes as a JSON file
        '''
        import json
        import logging
        import os

        savefile = self.filename[:self.filename.rfind('.')] + '.json'
        full_file = os.path.join(
                os.path.dirname(__file__), '../JSON/') + savefile

        run_dict = {'time': self.time.tolist(),
                    'voltage': self.voltage.tolist(),
                    'duration': self.duration,
                    'voltage_extremes': self.voltage_extremes,
                    'num_beats': self.num_beats,
                    'beats': self.beats.tolist(),
                    'units': self.units}

        with open(full_file, 'w') as fp:
            json.dump(run_dict, fp, sort_keys=True, indent=4)

        logging.info('Saved JSON file successfully')
