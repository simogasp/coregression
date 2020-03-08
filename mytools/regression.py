import numpy as np
import scipy.optimize


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


def residuals(p, x, y):
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


def fit_sigmoid(x, y, verbose: bool = False, lower=-0.5, upper=2.5) -> tuple:
    x_norm, t_x = normalize(x, lower=0.3)
    y_norm, t_y = normalize(y, lower=0.3)

    p_guess = np.array([np.median(x_norm), np.median(y_norm), 1.0, 1.0], dtype=float)
    p, cov, infodict, mesg, ier = scipy.optimize.leastsq(residuals, p_guess, args=(x_norm, y_norm), full_output=True)

    x0, y0, c, k = p

    x0r = (x0 - t_x[1]) / t_x[0]
    y0r = (y0 - t_y[1]) / t_y[0]
    cr = c / t_y[0]
    kr = k * t_x[0]

    model = (x0r, y0r, cr, kr)

    if verbose:
        print('''\
            Normalized model
            x0 = {x0}
            y0 = {y0}
            c = {c}
            k = {k}
            asymptot = {tinf}
            flex = {flex},{fley}
            '''.format(x0=x0, y0=y0, c=c, k=k, flex=x0, fley=sigmoid(p, x0), tinf=c + y0))

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
    import datetime
    import matplotlib.pyplot as plt

    data = np.genfromtxt(fname='../italy-intensive_care.csv', delimiter=',', names=True)

    x_orig = data['day']
    y_orig = data['intensive_care']

    print(x_orig)
    print(y_orig)

    model, xp, pxp = fit_sigmoid(x_orig, y_orig, verbose=True)

    # Plot the results
    plt.plot(x_orig, y_orig, '.', xp, pxp, '-')
    locs, labels = plt.xticks()
    a = list((datetime.datetime(2020, 1, 1) + datetime.timedelta(days=int(v))).strftime("%d %b") for v in locs.tolist())
    plt.xticks(ticks=locs.tolist(), labels=a)
    plt.xlabel('x')
    plt.ylabel('y', rotation='horizontal')
    plt.grid(True)
    plt.show()
