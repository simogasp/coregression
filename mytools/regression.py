import numpy as np
import scipy.optimize
import mytools.date as dt


def list_to_wolfram(l: list) -> str:
    return '{' + ', '.join('{{{}, {}}}'.format(k[0], k[1]) for k in l) + '}'


def create_prediction_table(data: np.array, y_sigmoid: np.array, y_exponential: np.array) -> np.array:
    num_rows = min((np.size(data, 0), np.size(y_exponential, 0), np.size(y_sigmoid, 0)))

    table = np.array([dt.day_of_year_to_string(data['day'][: num_rows]),
                      data['intensive_care'][: num_rows].tolist(),
                      y_exponential[: num_rows].tolist(),
                      y_sigmoid[: num_rows].tolist()])
    tmp = table.transpose().copy()
    print(tmp)
    table = np.array(tmp, dtype=[('date', '<U20'), ('cases', '<U10'), ('exp', '<U10'), ('sigm', '<U10')])
    return table


def exponential(p: np.array, x: np.array) -> np.array:
    """
    Evaluate an exponential function in the form

    :math:`f(x) = e^{-k(x-x_0)} + y_0`.

    Args:
        p (np.array): the array of parameters of the exponential [x0, y0, k]
        x (np.array): an array of values

    Returns:
        y (np.array): the exponential values at given x

    """
    x0, y0, k = p
    y = np.exp(k * (x - x0)) + y0
    return y


def exponential_residuals(p, x, y):
    """

    Args:
        p (np.array): the array of parameters of the exponential [x0, y0, k]
        x (np.array): an array of values
        y (np.array): an array of expected values

    Returns:

    """
    return y - exponential(p, x)


def exponential_dumb_initial_guess(x, y) -> np.array:

    print(np.array([np.median(x), np.median(y), 1.0], dtype=float))
    return np.array([np.median(x), np.median(y), 1.0], dtype=float)


def denormalize_exponential_params(p, t_x, t_y) -> tuple:
    x0, y0, k = p

    y0r = (y0 - t_y[1]) / t_y[0]
    kr = k * t_x[0]
    x0r = ((x0 - t_x[1]) / t_x[0]) + (np.log(1 / t_x[0]) / kr)

    return x0r, y0r, kr


def fit_exponential(x, y, verbose: bool = False, lower=-0.5, upper=2.5) -> tuple:
    model, xp, pxp = fit_model(x, y, exponential, exponential_residuals, denormalize_exponential_params,
                               exponential_dumb_initial_guess, lower=lower, upper=upper)

    if verbose:
        x0, y0, k = model
        print('''\
            Exponential model
            x0 = {x0}
            y0 = {y0}
            k = {k}
            '''.format(x0=x0, y0=y0, k=k))

    return model, xp, pxp


def sigmoid(p: np.array, x: np.array) -> np.array:
    """
    Evaluate a sigmoid

    :math:`f(x) = \\frac{c}{1 + e^{-k(x-x_0)}}+y_0`.

    Args:
        p (np.array): the array of parameters of the sigmoid [x0, y0, c, k]
        x (np.array): an array of values

    Returns:
        y (np.array): the sigmoid values at given x

    """
    x0, y0, c, k = p
    y = c / (1 + np.exp(-k * (x - x0))) + y0
    return y


def sigmoid_get_flex(p: np.array) -> tuple:
    flex_x = p[0]
    return flex_x, sigmoid(p, flex_x)


def sigmoid_residuals(p, x, y):
    """

    Args:
        p ():
        x ():
        y ():

    Returns:

    """
    return y - sigmoid(p, x)


def normalize(arr: np.array, lower: float = 0.0, upper: float = 1.0) -> tuple:
    """
    Normalize the input data in a range given by [lower, upper]

    :code:`arrNorm, t = normalize(arr, lower, upper)`

    Args:
        arr (np.array): the input data array
        lower (float): the minimum value of the new range
        upper (float): the maximum value of the new range

    Returns:
        (tuple): tuple containing:

            arrNorm (np.array) : the normalized data
            t (np.array) : the corresponding linear transformation s.t. :code:`arrNorm = t[0] * arr + t[1]`

    """

    arr = arr.copy()
    if lower > upper:
        lower, upper = upper, lower

    alpha = (upper - lower) / (arr.max() - arr.min())
    t = np.array([alpha, lower - arr.min() * alpha], dtype='float')

    arr = t[0] * arr + t[1]

    return arr, t


def normalize_back(arr: np.array, t: np.array) -> np.array:
    """

    Args:
        arr ():
        t ():

    Returns:

    """
    return (arr - t[1]) / t[0]


def fit_model(x, y, fun: callable, residual_fun: callable, denormalize_p: callable, guess: callable, lower=-0.5,
              upper=2.5) -> tuple:
    x_norm, t_x = normalize(x, lower=0.3)
    y_norm, t_y = normalize(y, lower=0.3)

    p_guess = guess(x_norm, y_norm)
    result = scipy.optimize.least_squares(residual_fun, p_guess, args=(x_norm, y_norm), verbose=1, loss='soft_l1')

    p = result.x

    model = denormalize_p(p, t_x, t_y)

    xp = np.linspace(lower, upper, 1500)
    pxp = fun(p, xp)

    xp = normalize_back(xp, t_x)
    pxp = normalize_back(pxp, t_y)

    return model, xp, pxp


def denormalize_sigmoid_params(p, t_x, t_y) -> tuple:
    x0, y0, c, k = p

    x0r = (x0 - t_x[1]) / t_x[0]
    y0r = (y0 - t_y[1]) / t_y[0]
    cr = c / t_y[0]
    kr = k * t_x[0]

    return x0r, y0r, cr, kr


def sigmoid_dumb_initial_guess(x, y) -> np.array:
    return np.array([np.median(x), np.median(y), 1.0, 1.0], dtype=float)


def fit_sigmoid(x, y, verbose: bool = False, lower=-0.5, upper=2.5) -> tuple:
    x_norm, t_x = normalize(x, lower=0.3)
    y_norm, t_y = normalize(y, lower=0.3)

    p_guess = sigmoid_dumb_initial_guess(x_norm, y_norm)
    # p, cov, infodict, mesg, ier = scipy.optimize.leastsq(residuals, p_guess, args=(x_norm, y_norm), full_output=True)
    result = scipy.optimize.least_squares(sigmoid_residuals, p_guess, args=(x_norm, y_norm), verbose=1, loss='soft_l1')
    p = result.x

    model = denormalize_sigmoid_params(p, t_x, t_y)

    if verbose:
        x0, y0, c, k = p
        print('''\
            Normalized model
            x0 = {x0}
            y0 = {y0}
            c = {c}
            k = {k}
            asymptot = {tinf}
            flex = {flex},{fley}
            '''.format(x0=x0, y0=y0, c=c, k=k, flex=x0, fley=sigmoid(p, x0), tinf=c + y0))

        x0r, y0r, cr, kr = model
        print('''\
            Sigmoid model
            x0 = {x0}
            y0 = {y0}
            c = {c}
            k = {k}
            asymptot = {tinf}
            flex = {flex},{fley}
            '''.format(x0=x0r, y0=y0r, c=cr, k=kr, flex=x0r, fley=sigmoid(model, x0r), tinf=cr + y0r))

    xp = np.linspace(lower, upper, 1500)
    pxp = sigmoid(p, xp)

    xp = normalize_back(xp, t_x)
    pxp = normalize_back(pxp, t_y)

    return model, xp, pxp


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    x_orig = data['day']
    y_orig = data['intensive_care']

    print(x_orig)
    print(y_orig)

    model, xp, pxp = fit_sigmoid(x_orig, y_orig, verbose=True)

    exp_model, exp_xp, exp_pxp = fit_exponential(x_orig, y_orig, verbose=True, upper=1.25)

    flex = sigmoid_get_flex(model)

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
