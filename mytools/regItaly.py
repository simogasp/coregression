import numpy as np
import mytools.regression as reg
import mytools.date as dt
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = np.genfromtxt(fname='italy-intensive_care.csv', delimiter=',', names=True)

    x_orig = data['day']
    y_orig = data['intensive_care']

    print(x_orig)
    print(y_orig)

    model, xp, pxp = reg.fit_sigmoid(x_orig, y_orig, verbose=True)

    der_model, der_xp, der_pxp = reg.fit_logistic_distribution(x_orig, y_orig, verbose=True)

    exp_model, exp_xp, exp_pxp = reg.fit_exponential(x_orig, y_orig, verbose=True, upper=1.25)

    exp_res = reg.exponential_residuals(p=exp_model, x=x_orig, y=y_orig)
    print(exp_res)
    print('std err exp: ' + str(np.std(exp_res)))

    sigm_res = reg.sigmoid_residuals(p=model, x=x_orig, y=y_orig)
    print(sigm_res)
    print('std err sigm: ' + str(np.std(sigm_res)))

    flex = reg.sigmoid_get_flex(model)

    der_res = reg.logistic_distribution_residuals(p=der_model, x=x_orig, y=y_orig)
    print(der_res)
    print('std err der sigm: ' + str(np.std(der_res)))

    peak = reg.logistic_distribution_get_max(der_model)

    # Plot the results
    plt.plot(x_orig, y_orig, '.', label='Intensive care cases')
    plt.plot(xp, pxp, '-', label='fitting sigmoid')
    plt.plot(exp_xp, exp_pxp, '-', label='fitting exponential')
    plt.plot(der_xp, der_pxp, '-', label='fitting sigmoid derivative')
    plt.plot(flex[0], flex[1], '.',
             label='Inflection point (' + dt.day_of_year_to_date(flex[0]).strftime("%d %b") + ' ' + '{:.2f}'.format(
                 flex[1]) + ' cases)')
    plt.plot(peak[0], peak[1], '.',
             label='peak (' + dt.day_of_year_to_date(peak[0]).strftime("%d %b") + ' ' + '{:.2f}'.format(
                 peak[1]) + ' cases)')
    locs, labels = plt.xticks()
    a = list((dt.day_of_year_to_date(v)).strftime("%d %b") for v in locs.tolist())
    plt.xticks(ticks=locs.tolist(), labels=a)

    plt.ylabel('cases', rotation='vertical')
    plt.grid(True)
    plt.title('Italy - Intensive care patients')
    plt.legend(loc='upper left')
    # plt.yscale('log')
    plt.show()
