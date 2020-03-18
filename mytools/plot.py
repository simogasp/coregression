import mytools.date as dt
import mytools.regression as reg
import pandas as pd
import plotly.graph_objs as go
import numpy as np


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

    days = data_frame.index

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=days,
            ticktext=dt.day_of_year_to_string(days),
            tickangle=90
        )
    )

    return iplot_add_log_scale_button(fig)


def iplot_analysis_plot(data_frame, title: str, exp_fitting: bool = True, sigm_fitting: bool = True,
                        log_fitting: bool = True):
    day_col = 'day'
    exp_col = 'exp'
    sigm_col = 'sigm'
    log_col = 'log'
    cases_col = data_frame.columns[1]

    x_orig = data_frame[day_col]
    y_orig = data_frame[cases_col]

    # preparing table with predictions
    d_max = x_orig.max()
    d_min = x_orig.min()

    df_final = data_frame

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
