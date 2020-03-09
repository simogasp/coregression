import numpy as np
import mytools.regression as reg
import mytools.date as dt


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    x_orig = data['day']
    y_orig = data['intensive_care']

    print(x_orig)
    print(y_orig)

    model, xp, pxp = reg.fit_sigmoid(x_orig, y_orig, verbose=True)

    exp_model, exp_xp, exp_pxp = reg.fit_exponential(x_orig, y_orig, verbose=True, upper=1.25)

    flex = reg.sigmoid_get_flex(model)

    # Plot the results
    plt.plot(x_orig, y_orig, '.', label='Intensive care cases')
    plt.plot(xp, pxp, '-', label='fitting sigmoid')
    plt.plot(exp_xp, exp_pxp, '-', label='fitting exponential')
    plt.plot(flex[0], flex[1], '.',
             label='Inflection point (' + dt.day_of_year_to_date(flex[0]).strftime("%d %b") + ' ' + '{:.2f}'.format(
                 flex[1]) + ' cases)')
    locs, labels = plt.xticks()
    a = list((dt.day_of_year_to_date(v)).strftime("%d %b") for v in locs.tolist())
    plt.xticks(ticks=locs.tolist(), labels=a)

    plt.ylabel('cases', rotation='vertical')
    plt.grid(True)
    plt.title('Italy - Intensive care patients')
    plt.legend(loc='upper left')
    plt.show()