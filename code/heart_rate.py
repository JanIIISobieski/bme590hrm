from numpy import amin, amax
import pandas
import logging
import matplotlib.pyplot as plt
import os


class ECG:
    '''Class to describe ECG trace data

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
    def __init__(self, filename='test_data1.csv', analyze=True):
        '''__init__ method of the ECG class

        :param filename (str, default='test_data1.csv'): CSV file containing
            ECG trace data. Filename should include the .csv extension.
            File by default should be in a 'test_data' folder one level higher
            than where the module resides
        :param analyze (boolean, default=True): runs all class methods during
            initialization. If set to false, only imports time and voltage data
        '''
        self.filename = filename
        self.import_csv()
        if analyze:
            self.find_volt_extrema()
            self.find_duration()
        pass

    def import_csv(self):
        '''Class method to import CSV

        :return time (array): array of the sampled times in ECG trace
        :return voltage (array): array of the sampled voltages in ECG trace
        '''
        full_file = os.path.join(os.path.dirname(__file__), '../test_data/',
                                 self.filename)
        imported_file = pandas.read_csv(full_file,
                                        header=None,
                                        names=['time', 'voltage'],
                                        skipinitialspace=True)
        self.time = imported_file.time.values
        self.voltage = imported_file.voltage.values

    def find_mean_hr_bpm(self, time_dur=1):
        pass

    def find_volt_extrema(self):
        '''Class method to find the voltage extremes in ECG trace

        :return voltage_extremes (tuple): the minimum and maximum voltage
            values sampled
        '''
        self.voltage_extremes = (amin(self.voltage), amax(self.voltage))

    def find_duration(self):
        '''Class method to find the duration of ECG trace

        :return duration (float): the total time of the sampled ECG
        '''
        self.duration = self.time[-1] - self.time[0]

    def find_num_beats(self):
        pass

    def find_beats(self):
        pass

    def export_json():
        pass
