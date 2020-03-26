import numpy as np
import mytools.regression as reg
import mytools.date as dt
import mytools.plot as mpl
import mytools.dataio as io
import matplotlib.pyplot as plt

if __name__ == "__main__":

    region = 'Veneto'
    category = 'terapia_intensiva'

    regions = io.italy_load_regions([region])

    intensive = io.italy_regions_filter_by_category(regions, category)

    condition = intensive[region] > 0
    x_orig = np.array(mpl.get_days(intensive[condition]))
    y_orig = intensive[condition][region]

    mpl.matplot_analysis_plot(x_orig, y_orig, title=region+' - '+category, category=category)

    category = 'totale_casi'
    total_cases = io.italy_regions_filter_by_category(regions, category)

    condition = total_cases[region] > 0
    x_orig = np.array(mpl.get_days(total_cases[condition]))
    y_orig = total_cases[condition][region]

    mpl.matplot_analysis_plot(x_orig, y_orig, title=region+' - '+category, category=category, log_fitting=False)

    regions = io.italy_load_regions()
    total_cases = io.italy_regions_filter_by_category(regions, category)

    mpl.matplot_comparative_plot(total_cases, title='Italy ' + category + ' by regions')

    mpl.matplot_comparative_plot(total_cases, title='Italy ' + category + ' by regions', min_common=20)

    category = 'deceduti'
    deaths = io.italy_regions_filter_by_category(regions, category)

    mpl.matplot_comparative_plot(deaths, title='Italy ' + category + ' by regions')

    mpl.matplot_comparative_plot(deaths, title='Italy ' + category + ' by regions', min_common=20)

