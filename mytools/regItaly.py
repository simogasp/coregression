import numpy as np
import mytools.plot as mpl
import mytools.dataio as io


if __name__ == "__main__":
    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    category = 'intensive_care'
    x_orig = data['day']
    y_orig = data[category]

    mpl.matplot_analysis_plot(x_orig, y_orig, title='Italy - intensive care cases', category='intensive care')

    italy = io.italy_load_whole_country()
    category = 'totale_attualmente_positivi'
    view_category = io.italy_country_filter_by_category(italy, categories=[category])

    x_orig = np.array(mpl.get_days(view_category))
    y_orig = view_category[category]

    mpl.matplot_analysis_plot(x_orig, y_orig, title='Italy - ' + category, category=category, log_fitting=False)


    category = 'deceduti'
    view_category = io.italy_country_filter_by_category(italy, categories=[category])

    x_orig = np.array(mpl.get_days(view_category))
    y_orig = view_category[category]

    mpl.matplot_analysis_plot(x_orig, y_orig, title='Italy - ' + category, category=category)
