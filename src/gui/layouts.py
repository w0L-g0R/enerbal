# from files.energiebilanzen.processing.eb_sheets import eb_sheets
# from settings import eb_indices

import plotly.graph_objects as go


def get_graph_layout(unit: str, title: str, barmode: str = "stacked"):

    top_margin_factor = title.count(" <br> ")
    print('top_margin_factor: ', top_margin_factor)

    top_margin = 32 + 24 * top_margin_factor

    return go.Layout(
        title=dict(
            text=title,
            y=.97,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font_size=16,
            font_family="Quicksand",
        ),
        modebar=dict(orientation="v"),
        barmode=barmode,
        showlegend=True,
        legend=dict(x=-0.1, y=-0.15),
        legend_orientation="h",
        template="plotly_white",
        margin=dict(l=12, r=24, t=top_margin, b=0),
        # margin=dict(pad=24),
        width=496,
        height=400,
        yaxis_title=unit,
        font=dict(family="Quicksand, sans-serif",
                  size=12, color="black"),

        xaxis=dict(
            dtick=1,
            tickangle=90,
            showticklabels=True,
            zeroline=True,
        ),
        yaxis=dict(
            ticks="outside",
            tickcolor="lightgrey",
            ticklen=5,
            zeroline=True,
            titlefont=dict(
                family='Oswald, sans-serif',
                size=14,
                color='lightgrey'
            ),

        ),
    )

# def get_layout_with_datetime(unit: str, title: str, height: int = 360):

#     return go.Layout(
#         # title=dict(text=title, y=0.98, x=0.5,
#         #            xanchor="center", yanchor="top"),
#         # title=title,
#         barmode="stack",
#         # hoverlabel=dict(bgcolor="white", font_size=14,
#         #                 font_family="Quicksand"),
#         # legend=dict(
#         #     # yanchor='bottom',
#         #     # xanchor="center",
#         #     y=-0.18,
#         #     x=0.5,
#         #     # x=-.1,
#         #     # y=-0.1,
#         #     font=dict(family="Arial, sans-serif",
#         #               size=12, color="black"),
#         #     # bordercolor="whitesmoke",
#         #     # borderwidth=1,
#         # ),
#         # font=dict(family="Arial, sans-serif",
#         #           size=12, color="black"),
#         # paper_bgcolor="black",
#         # plot_bgcolor="black",
#         width=432,
#         # autosize=True,
#         height=440,
#         # margin=dict(l=48, r=48, t=24, b=0, pad=0),
#         # margin=dict(autoexpan),
#         showlegend=True,
#         legend_orientation="h",
#         template="plotly_white",
#         yaxis=dict(
#             ticks="outside",
#             # tickcolor="black",
#             ticklen=10,
#             # ticksuffix=" " + unit,
#             showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#         ),
#         xaxis=dict(
#             # ticks="outside",
#             # tickcolor="black",
#             # ticklen=10,
#             # ticksuffix=" " + unit,
#             # showticksuffix="all",
#             # domain=[0, 0.7]
#             zeroline=True,
#             # zeroline_color="black",
#         ),
#     )
