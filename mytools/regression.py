import datetime

import numpy as np
import matplotlib.pyplot as plt
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
    if lower > upper: lower, upper = upper, lower

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


if __name__ == "__main__":
    # raw data
    # x = np.array([821,576,473,377,326],dtype='float')
    # y = np.array([255,235,208,166,157],dtype='float')

    day_start = 55
    day_stop = 66

    x_orig = np.arange(start=day_start, stop=day_stop, step=1, dtype=float)
    y_orig = np.array([27, 35, 35, 56, 64, 105, 140, 166, 229, 295, 351], dtype='float')
    print(x_orig)
    print(y_orig)

    x, t_x = normalize(x_orig, lower=0.3)
    y, t_y = normalize(y_orig, lower=0.3)

    print(x)
    print(y)

    p_guess = np.array([np.median(x), np.median(y), 1.0, 1.0], dtype=float)
    p, cov, infodict, mesg, ier = scipy.optimize.leastsq(residuals, p_guess, args=(x, y), full_output=True)

    x0, y0, c, k = p
    print('''\
    x0 = {x0}
    y0 = {y0}
    c = {c}
    k = {k}
    '''.format(x0=x0, y0=y0, c=c, k=k))

    # xp = np.linspace(day_start-5, day_stop+200, 1500)
    xp = np.linspace(0, 2.5, 1500)
    pxp = sigmoid(p, xp)

    # xp = resize_back(xp, x_orig, lower=0.3)
    xp = normalize_back(xp, t_x)
    # print(xp)
    # pxp = resize_back(pxp, y_orig, lower=0.3)
    pxp = normalize_back(pxp, t_y)
    # print(pxp)

    # print(resize_back(x, x_orig, lower=0.3))
    # print(resize_back(y, y_orig, lower=0.3))

    x0r = (x0 - t_x[1] / t_x[0])
    y0r = (y0 - t_y[1]) / t_y[0]
    cr = c / t_y[0]
    kr = k * t_x[0]

    print('''\
    x0 = {x0}
    y0 = {y0}
    c = {c}
    k = {k}
    asymptot = {tinf}
    flex = {flex},{fley}
    '''.format(x0=x0r, y0=y0r, c=cr, k=kr, flex=kr * x0r / cr, fley=sigmoid(p, kr * x0r / cr), tinf=cr + y0r))

    # Plot the results
    # plt.xkcd(scale=1.015)
    plt.plot(x_orig, y_orig, '.', xp, pxp, '-')
    locs, labels = plt.xticks()
    a = list((datetime.datetime(2020, 1, 1) + datetime.timedelta(days=int(v))).strftime("%d %b") for v in locs.tolist())
    plt.xticks(ticks=locs.tolist(), labels=a)
    plt.xlabel('x')
    plt.ylabel('y', rotation='horizontal')
    plt.grid(True)
    plt.show()
