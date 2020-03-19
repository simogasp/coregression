import numpy as np
import mytools.plot as mpl


if __name__ == "__main__":
    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    category = 'intensive_care'
    x_orig = data['day']
    y_orig = data[category]

    mpl.matplot_analysis_plot(x_orig, y_orig, title='Italy - intensive care cases', category='intensive care')