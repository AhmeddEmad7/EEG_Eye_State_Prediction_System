
#
# import pyqtgraph
# # import qdarkstyle
# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from PyQt6.uic import loadUiType
# from os import path
# import sys
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import scipy.stats as stats
# import scipy.signal
# # import pyeeg

import pyqtgraph
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import numpy as np
import os
from os import path
import sys
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import scipy.stats as stats
import scipy.signal

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main3.ui"))



class MainApp(QMainWindow, FORM_CLASS):
    Fs = 128

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pyqtgraph.setConfigOptions(antialias=True)

        # Unfiltered Data
        # self.data = pd.read_csv("/Users/nourhanahmed2002/Desktop/instruments/EEG_Eye_State_Classification.csv")
        self.data = pd.read_csv("C:\PyCharm\instruemnts task2\EEG_Eye_State_Classification.csv")
        self.Y = self.data['eyeDetection']
        self.X = self.data.iloc[:, [1, 2, 4]]
        self.calculate_and_print_features(self.X)
        # print(self.X)
        # print(self.Y)
        self.graphicsView_3.setCentralWidget(pyqtgraph.PlotItem())
        # self.plot_data([self.X], xlim=[2, 20], ylim=[-2, 12]  )
        # self.plot_data([self.X],  xlim=[0, len(self.X) / self.Fs], ylim=[-10, 30] )
        # # self.plot_data([self.X],  xlim=[0, len(self.X) / self.Fs], ylim=[0, 7500]  )
        # y_min = self.X.min().min()
        # y_max = self.X.max().max()
        # y_range = y_max - y_min
        # self.plot_data([self.X], xlim=[0, len(self.X) / self.Fs], ylim=[y_min - 0.1 * y_range, y_max + 0.1 * y_range])
        self.plot_data([self.X],  xlim=[0, len(self.X) / self.Fs], ylim=[-40, 60]  )


        #Filtered Data
        self.filtered_data = pd.read_csv(r"C:\users\hanah\Downloads\eeg_data_corrected.csv")

        self.Y2 = self.filtered_data['eyeDetection']
        self.X2 = self.filtered_data.iloc[:, [1, 2, 4]]

        self.graphicsView_2.setCentralWidget(pyqtgraph.PlotItem())
        # self.plot_filtered_data([self.X2], xlim=[2, 20], ylim=[-2, 12])
        # self.plot_filtered_data([self.X2], xlim=[0, len(self.X) / self.Fs], ylim=[-2, 12])
        # self.plot_filtered_data([self.X2], xlim=[0, 120], ylim=[-10, 30])
        self.plot_filtered_data([self.X2], xlim=[0, len(self.X2) / self.Fs], ylim=[-40, 60])
        self.calculate_and_print_features(self.X2)




    def plot_data(self, X, xlim=[2, 20], ylim=[-2, 12]):
        plot_widget = self.graphicsView_3.centralWidget
        plot_widget.addLegend()

        for ind_data, data in enumerate(X):
            t = np.arange(0, len(data) * 1 / self.Fs, 1 / self.Fs)
            columns = data.columns.tolist()

            if columns:  # Check if there are columns in data
                custom_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Define custom RGB colors
                for ind, col in enumerate(columns):
                    pen_color = custom_colors[ind % len(custom_colors)]  # Reuse colors if needed
                    pen = pyqtgraph.mkPen(color=pen_color)
                    plot_widget.plot(t, 5 * ind + stats.zscore(data[col], nan_policy='omit'),
                                     pen=pen, name=col)
                    # print(col)
                    # plot_widget.addLegend()
            else:
                print("No columns in the data.")

        plot_widget.setTitle("Data")
        # plot_widget.addLegend()
        plot_widget.showGrid(True, True)
        plot_widget.setXRange(xlim[0], xlim[1])
        plot_widget.setYRange(ylim[0], ylim[1])



    def plot_filtered_data(self, X, xlim=[2, 20], ylim=[-2, 12]):
        plot_widget = self.graphicsView_2.centralWidget
        plot_widget.addLegend()

        for ind_data, data in enumerate(X):
            t = np.arange(0, len(data) * 1 / self.Fs, 1 / self.Fs)
            columns = data.columns.tolist()

            if columns:  # Check if there are columns in data
                custom_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Define custom RGB colors
                for ind, col in enumerate(columns):
                    pen_color = custom_colors[ind % len(custom_colors)]  # Reuse colors if needed
                    pen = pyqtgraph.mkPen(color=pen_color)
                    plot_widget.plot(t, 5 * ind + stats.zscore(data[col], nan_policy='omit'),
                                     pen=pen, name=col)
            else:
                print("No columns in the data.")

        plot_widget.setTitle("Data")
        # plot_widget.addLegend()
        plot_widget.showGrid(True, True)
        plot_widget.setXRange(xlim[0], xlim[1])
        plot_widget.setYRange(ylim[0], ylim[1])

    def calculate_and_print_features(self, data):
            columns = data.columns.tolist()
            # print(columns)

            if columns:  # Check if there are columns in data
                for ind, col in enumerate(columns):
                    signal = data[col].to_numpy()
                    # Calculate and print the statistical measures
                    mean_value = np.mean(signal)
                    variance = np.var(signal)
                    # mean_value = np.mean(signal[:10])
                    # variance = np.var(signal[:10])

                    print(f"Signal {col} Features:")
                    print(f"Mean: {mean_value}")
                    print(f"Variance: {variance}")
                    # Calculate and print Power Spectral Density (PSD)
                    f, Pxx = scipy.signal.welch(signal, fs=self.Fs)
                    print(f"Power Spectral Density (PSD) for Signal {col}:")
                    # print(f"Frequencies: {f}")
                    # # print(len(f))
                    # print(f"PSD Values: {Pxx}")
                    print(f"Frequencies: {f[:10]}")
                    # print(len(f))
                    print(f"PSD Values: {Pxx[:10]}")
                    # print(np.sum(Pxx))
                    # print(len(Pxx))

                    # Calculate and print Band Power Ratios
                    band_power_alpha = np.trapz(Pxx[(f >= 8) & (f <= 13)])  # Alpha band
                    band_power_beta = np.trapz(Pxx[(f >= 13) & (f <= 30)])  # Beta band
                    total_power = np.trapz(Pxx)  # Total power
                    print(f"Band Power Ratios for Signal {col}:")
                    print(f"Alpha Band Power: {band_power_alpha}")
                    print(f"Beta Band Power: {band_power_beta}")
                    print(f"Total Power: {total_power}")
                    print(f"Alpha/Beta Ratio: {band_power_alpha / band_power_beta}")
                    print("-----------------------------------------------------------------")
            else:
                print("No columns in the data.")

    def initializeUI(self):
        self.setWindowTitle("Multi-Channel Signal Viewer")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    app.exec()


if __name__ == '__main__':
    main()