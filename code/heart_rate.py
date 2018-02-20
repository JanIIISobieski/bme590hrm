class ECG:
    def __init__(self, filename='test_data1.csv'):
        self.filename = filename
        self.import_csv()
        self.find_volt_extrema()
        self.find_duration()
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
        pass

    def find_beats(self):
        import matplotlib.pyplot as plt
        from scipy import signal
        from numpy import arange
        peakind = signal.find_peaks_cwt(self.voltage,
                                        arange(1, 50),
                                        min_snr=20)
        plt.figure
        plt.plot(self.time, self.voltage)
        plt.plot(self.time[peakind], self.voltage[peakind], 'o')
        pass

    def export_json():
        pass
