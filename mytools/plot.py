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


def iplot_analysis_plot(data_frame, title: str):
    data_frame['day'] = data_frame.index

    x_orig = data_frame['day']
    y_orig = data_frame.iloc[:, 0]

    sigm_model, xp, pxp = reg.fit_sigmoid(x_orig, y_orig, verbose=True)
    flex = reg.sigmoid_get_flex(sigm_model)

    exp_model, exp_xp, exp_pxp = reg.fit_exponential(x_orig, y_orig, upper=1.25, verbose=True)

    # preparing table with predictions
    d_max = x_orig.max()
    d_min = x_orig.min()

    f_days_exp = range(d_min - 4, d_max + 4, 1)
    f_days_sigm = range(d_min - 4, d_max + 20, 1)

    f_exp = reg.exponential(exp_model, f_days_exp)
    f_sigm = reg.sigmoid(sigm_model, f_days_sigm)
    f_df_exp = pd.DataFrame({'day': f_days_exp, 'exp': f_exp})
    f_df_sigm = pd.DataFrame({'day': f_days_sigm, 'sigm': f_sigm})
    f_df_exp.index = dt.day_of_year_to_string(f_days_exp)
    f_df_sigm.index = dt.day_of_year_to_string(f_days_sigm)

    df_final = pd.merge(data_frame, f_df_exp, on='day', how='outer', sort=True).merge(f_df_sigm, on='day', how='outer',
                                                                                      sort=True)
    df_final.index = dt.day_of_year_to_string(f_days_sigm)

    fig = df_final[['exp', 'sigm', data_frame.columns[0]]].iplot(theme="white", title=title, size=4,
                                                                 yTitle='case', mode='lines+markers', asFigure=True)
    fig.data[2].mode = 'markers'
    fig.data[2].marker.size = 8
    fig.add_trace(go.Scatter(x=[dt.day_of_year_to_string(round(flex[0]))], y=[flex[1]], name='flex', mode="markers"))
    fig.data[3].marker.size = 8
    fig.data[3].marker.color = 'rgba(255, 0, 0, 125)'

    return fig
