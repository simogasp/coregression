import mytools.date as dt


def iplot_add_log_scale_button(fig):
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=[{"yaxis.type": "linear"}], #"xaxis.type": "linear"}],
                        label="Linear",
                        method="relayout"
                    ),
                    dict(
                        args=[{"yaxis.type": "log"}], #"xaxis.type": "linear"}],
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

