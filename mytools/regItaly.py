import numpy as np
import mytools.regression as reg
import mytools.date as dt
import mytools.plot as mpl
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    category = 'intensive_care'
    x_orig = data['day']
    y_orig = data[category]

    mpl.matplot_analysis_plot(x_orig, y_orig, title='Italy - intensive care cases', category='intensive care')