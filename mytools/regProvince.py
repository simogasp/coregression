import numpy as np
import mytools.plot as mpl
import mytools.dataio as io

if __name__ == "__main__":

    province = 'Verona'
    category = 'totale_casi'

    provinces = io.italy_load_provinces(io.italy_get_filename_provinces(), [province])

    intensive = io.italy_provinces_filter_by_category(provinces, category)

    condition = intensive[province] > 0
    x_orig = np.array(mpl.get_days(intensive[condition]))
    y_orig = intensive[condition][province]

    mpl.matplot_analysis_plot(x_orig, y_orig, title=province+' - '+category, category=category, log_fitting=False)