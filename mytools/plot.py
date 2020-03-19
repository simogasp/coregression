import mytools.date as dt
import mytools.regression as reg
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
from typing import List


def iplot_add_log_scale_button(fig):
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear"}],  # "xaxis.type": "linear"}],
                        label="Linear",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log"}],  # "xaxis.type": "linear"}],
                        label="Log",
                        method="relayout"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ]
    )

    return fig


def iplot_comparative_plot(data_frame, title='Comparison of death cases', size=4, yTitle='cases', mode='lines+markers',
                           asFigure=True):
    fig = data_frame.iplot(theme="white", title=title, size=size, yTitle=yTitle, mode=mode, asFigure=asFigure)

    # days = data_frame.index
    #
    # fig.update_layout(
    #     xaxis=dict(
    #         tickmode='array',
    #         tickvals=days,
    #         ticktext=dt.day_of_year_to_string(days),
    #         tickangle=90
    #     )
    # )

    return iplot_add_log_scale_button(fig)


def get_days(data_frame: pd.DataFrame) -> List[int]:
    day_col = 'day'
    if day_col in data_frame.columns:
        if data_frame[day_col].dtype != 'str':
            return data_frame[day_col].tolist()
        else:
            raise TypeError('The day column is not a numeric value')

    dates = data_frame.index.tolist()
    if not all(isinstance(d, str) for d in dates):
        raise TypeError('The indexes seems not to be strings containing the dates')

    return dt.str_to_day_of_year(dates, dt.format_ddmmyy)


def iplot_analysis_plot(data_frame: pd.DataFrame, title: str, exp_fitting: bool = True, sigm_fitting: bool = True,
                        log_fitting: bool = True):
    """

    Args:
        data_frame (pd.DataFrame):  dataframe with 'day' and
        title ():
        exp_fitting ():
        sigm_fitting ():
        log_fitting ():

    Returns:

    """
    day_col = 'day'
    exp_col = 'exp'
    sigm_col = 'sigm'
    log_col = 'log'
    cases_col = data_frame.columns[0]

    x_orig = np.array(get_days(data_frame))
    y_orig = data_frame[cases_col]

    # preparing table with predictions
    d_max = x_orig.max()
    d_min = x_orig.min()

    df_final = data_frame
    df_final[day_col] = x_orig

    columns = []

    if exp_fitting:
        exp_model, exp_xp, exp_pxp = reg.fit_exponential(x_orig, y_orig, upper=1.25, verbose=True)
        f_days_exp = range(d_min - 4, d_max + 4, 1)
        f_exp = reg.exponential(exp_model, f_days_exp)
        f_df_exp = pd.DataFrame({day_col: f_days_exp, exp_col: f_exp})
        f_df_exp.index = dt.day_of_year_to_string(f_days_exp)
        df_final = pd.merge(df_final, f_df_exp, on=day_col, how='outer', sort=True)
        columns = columns + [exp_col]

    if sigm_fitting:
        sigm_model, xp, pxp = reg.fit_sigmoid(x_orig, y_orig, verbose=True)
        flex = reg.sigmoid_get_flex(sigm_model)
        f_days_sigm = range(d_min - 4, d_max + 20, 1)
        f_sigm = reg.sigmoid(sigm_model, f_days_sigm)
        f_df_sigm = pd.DataFrame({day_col: f_days_sigm, sigm_col: f_sigm})
        f_df_sigm.index = dt.day_of_year_to_string(f_days_sigm)
        df_final = pd.merge(df_final, f_df_sigm, on=day_col, how='outer', sort=True)
        columns = columns + [sigm_col]

    if log_fitting:
        log_model, log_xp, log_pxp = reg.fit_logistic_distribution(x_orig, y_orig, verbose=True)
        peak = reg.logistic_distribution_get_max(log_model)
        f_days_log = range(d_min - 4, d_max + 20, 1)
        f_log = reg.logistic_distribution(log_model, f_days_log)
        f_df_log = pd.DataFrame({day_col: f_days_log, log_col: f_log})
        f_df_log.index = dt.day_of_year_to_string(f_days_log)
        df_final = pd.merge(df_final, f_df_log, on=day_col, how='outer', sort=True)
        columns = columns + [log_col]

    df_final.index = dt.day_of_year_to_string(df_final[day_col])

    columns = columns + [cases_col]

    fig = df_final[columns].iplot(theme="white", title=title, size=4, yTitle='case', mode='lines+markers',
                                  asFigure=True)
    if sigm_fitting:
        fig.add_trace(
            go.Scatter(x=[dt.day_of_year_to_string(round(flex[0]))], y=[flex[1]], name='flex', mode="markers"))
    if log_fitting:
        fig.add_trace(
            go.Scatter(x=[dt.day_of_year_to_string(round(peak[0]))], y=[peak[1]], name='peak', mode="markers"))

    for d in fig.data:
        if d.name == 'flex':
            d.marker.size = 8
            d.marker.color = 'rgba(255, 0, 0, 125)'

        if d.name == 'peak':
            d.marker.size = 8
            d.marker.color = 'rgba(255, 0, 0, 125)'

        if d.name == cases_col:
            d.mode = 'markers'
            d.marker.size = 8

    return fig


def matplot_analysis_plot(x_orig, y_orig, title: str, category: str, exp_fitting: bool = True, sigm_fitting: bool = True, log_fitting: bool = True, verbose: bool = True):

    if exp_fitting:
        exp_model, exp_xp, exp_pxp = reg.fit_exponential(x_orig, y_orig, verbose=True, upper=1.25)

        if verbose:
            exp_res = reg.exponential_residuals(p=exp_model, x=x_orig, y=y_orig)
            print(exp_res)
            print('std err exp: ' + str(np.std(exp_res)))

    if sigm_fitting:
        model, xp, pxp = reg.fit_sigmoid(x_orig, y_orig, verbose=True)
        sigm_res = reg.sigmoid_residuals(p=model, x=x_orig, y=y_orig)
        flex = reg.sigmoid_get_flex(model)
        if verbose:
            print(sigm_res)
            print('std err sigm: ' + str(np.std(sigm_res)))

    if log_fitting:
        der_model, der_xp, der_pxp = reg.fit_logistic_distribution(x_orig, y_orig, verbose=True)
        peak = reg.logistic_distribution_get_max(der_model)
        if verbose:
            der_res = reg.logistic_distribution_residuals(p=der_model, x=x_orig, y=y_orig)
            print(der_res)
            print('std err der sigm: ' + str(np.std(der_res)))



    # Plot the results
    if sigm_fitting:
        plt.plot(xp, pxp, '-', label='fitting sigmoid')
    if exp_fitting:
        plt.plot(exp_xp, exp_pxp, '-', label='fitting exponential')
    if log_fitting:
        plt.plot(der_xp, der_pxp, '-', label='fitting logistic distribution')

    plt.plot(x_orig, y_orig, '.', label=category)
    if sigm_fitting:
        plt.plot(flex[0], flex[1], '.',
                 label='Inflection point (' + dt.day_of_year_to_date(flex[0]).strftime("%d %b") + ' ' + '{:.2f}'.format(
                     flex[1]) + ' cases)')
    if log_fitting:
        plt.plot(peak[0], peak[1], '.', label='peak (' + dt.day_of_year_to_date(peak[0]).strftime("%d %b") + ' ' + '{:.2f}'.format( peak[1]) + ' cases)')

    locs, labels = plt.xticks()
    a = list((dt.day_of_year_to_date(v)).strftime("%d %b") for v in locs.tolist())
    plt.xticks(ticks=locs.tolist(), labels=a)

    plt.ylabel('cases', rotation='vertical')
    plt.grid(True)
    plt.title(title)
    plt.legend(loc='upper left')
    # plt.yscale('log')
    plt.show()
