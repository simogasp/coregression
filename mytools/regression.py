import numpy as np
import scipy.optimize
import mytools.date as dt
from math import sqrt, log


def list_to_wolfram(data: list) -> str:
    return '{' + ', '.join('{{{}, {}}}'.format(k[0], k[1]) for k in data) + '}'


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

    :math:`f(x) = e^{k(x-x_0)} + y_0`.

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
    x0r = ((x0 - t_x[1]) / t_x[0]) - (np.log(1 / t_y[0]) / kr)

    return x0r, y0r, kr


def fit_exponential(x, y, verbose: bool = False, lower=-0.5, upper=2.5) -> tuple:
    model, xp, pxp = fit_model(x, y, exponential, exponential_residuals, denormalize_exponential_params,
                               exponential_dumb_initial_guess, lower=lower, upper=upper, verbose=verbose)

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


def sigmoid_first_derivative(p: np.array, x: np.array) -> np.array:
    """
    Evaluate the derivative of the sigmoid

    :math:`f(x) = \\frac{c}{1 + e^{-k(x-x_0)}}+y_0`

    as

    :math:`\\frac{d f(x)}{dx} = f(x)(1 - f(x))`

    Args:
        p (np.array): the array of parameters of the sigmoid [x0, y0, c, k]
        x (np.array): an array of values where to evaluate the first derivative

    Returns:
        y (np.array): the first derivative values at given x

    """
    x0, y0, c, k = p
    e = np.exp(-k * (x - x0))
    return (c * k * e) / ((e + 1) ** 2)


def sigmoid_first_derivative_less_than(p: np.array, alpha: float) -> tuple:
    x0, y0, c, k = p
    a = sqrt(c ** 2 * k ** 2 - 4 * alpha * c * k) / (2 * alpha)
    b = (c * k - 2 * alpha) / (2 * alpha)
    z1 = a + b
    z2 = - (a - b)

    return x0 - log(z1) / k, x0 - log(z2) / k


def sigmoid_get_flex(p: np.array) -> tuple:
    flex_x = p[0]
    return flex_x, sigmoid(p, flex_x)


def sigmoid_get_asymptote(p: np.array) -> tuple:
    x0, y0, c, k = p
    return y0, c + y0


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
              upper=2.5, verbose=False) -> tuple:
    x_norm, t_x = normalize(x, lower=0.3)
    y_norm, t_y = normalize(y, lower=0.3)

    p_guess = guess(x_norm, y_norm)
    result = scipy.optimize.least_squares(residual_fun, p_guess, args=(x_norm, y_norm), verbose=verbose, loss='soft_l1')

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
    model, xp, pxp = fit_model(x, y, sigmoid, sigmoid_residuals, denormalize_sigmoid_params,
                               sigmoid_dumb_initial_guess, lower=lower, upper=upper, verbose=verbose)

    x0r, y0r, cr, kr = model
    print('''\
        Sigmoid model
        x0 = {x0}
        y0 = {y0}
        c = {c}
        k = {k}
        asymptot = {tinf}
        flex = {flex}, {fley}
        '''.format(x0=x0r, y0=y0r, c=cr, k=kr, flex=x0r, fley=sigmoid(model, x0r), tinf=cr + y0r))

    return model, xp, pxp


def logistic_distribution(p: np.array, x: np.array) -> np.array:
    """
    Evaluate the derivative of the sigmoid

    :math:`f(x) = \\frac{c}{1 + e^{-k(x-x_0)}}+y_0`

    as

    :math:`\\frac{d f(x)}{dx} = f(x)(1 - f(x))`

    Args:
        p (np.array): the array of parameters of the sigmoid [x0, y0, c, k]
        x (np.array): an array of values where to evaluate the first derivative

    Returns:
        y (np.array): the first derivative values at given x

    """
    x0, y0, c, k = p
    e = np.exp(-k * (x - x0))
    return (c * k * e) / ((e + 1) ** 2) + y0


def logistic_distribution_residuals(p, x, y):
    """

    Args:
        p ():
        x ():
        y ():

    Returns:

    """
    return y - logistic_distribution(p, x)


def fit_logistic_distribution(x, y, verbose: bool = False, lower=-0.5, upper=2.5) -> tuple:
    model, xp, pxp = fit_model(x, y, logistic_distribution, logistic_distribution_residuals,
                               denormalize_logistic_distribution_params,
                               sigmoid_dumb_initial_guess, lower=lower, upper=upper, verbose=verbose)

    x0r, y0r, cr, kr = model
    print('''\
        Sigmoid derivative model
        x0 = {x0}
        y0 = {y0}
        c = {c}
        k = {k}
        max = {flex}, {fley}
        '''.format(x0=x0r, y0=y0r, c=cr, k=kr, flex=x0r, fley=sigmoid(model, x0r)))

    return model, xp, pxp


def denormalize_logistic_distribution_params(p, t_x, t_y) -> tuple:
    x0, y0, c, k = p

    x0r = (x0 - t_x[1]) / t_x[0]
    y0r = (y0 - t_y[1]) / t_y[0]
    cr = c / (t_y[0] * t_x[0])
    kr = k * t_x[0]

    return x0r, y0r, cr, kr


def logistic_distribution_get_max(p) -> tuple:
    x0, y0, c, k = p

    return x0, c * k / 4 + y0
