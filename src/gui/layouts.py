# from files.energiebilanzen.convert.eb_sheets import eb_sheets
# from settings import eb_indices

import plotly.graph_objects as go


def get_graph_layout(y_unit: str, x_unit: str, title: str,
                     barmode: str = "relative"):

    top_margin_factor = title.count(" <br> ")
    top_margin = 32 + 24 * top_margin_factor

    return go.Layout(
        title=dict(
            text=title,
            y=.96,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font_size=16,
            font_family="Quicksand",
        ),
        modebar=dict(orientation="v"),
        barmode=barmode,
        showlegend=True,
        legend=dict(x=0, y=-0.5, xanchor="center", yanchor="bottom", ),
        legend_orientation="h",
        # template="plotly_dark",
        margin=dict(l=0, r=24, t=top_margin, b=12),
        # margin=dict(l=12, r=24, t=top_margin, b=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # margin="auto",
        autosize=True,
        # width=364,
        # height=400,
        xaxis_title=x_unit,
        yaxis_title=y_unit,
        font=dict(family="Quicksand, sans-serif",
                  size=13, color="white"),

        xaxis=dict(
            dtick=1,
            autorange=True,
            tickangle=90,
            tickmode="auto",
            showticklabels=True,
            zeroline=True,
            showgrid=True,
            gridwidth=0.5,
            gridcolor='#444444',
            zerolinewidth=3,
            zerolinecolor='white',
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            tickmode="auto",
            gridcolor='#444444',
            ticks="outside",
            tickcolor="#444444",
            ticklen=2,
            zeroline=True,
            zerolinewidth=3,
            zerolinecolor='white',
            autorange=True,
            # titlefont=dict(
            #     family='Oswald, sans-serif',
            #     size=14,
            #     color='lightgrey'
            # ),

        ),
    )

    # fig.update_layout(
    #     xaxis=dict(

    #     ),
    #     yaxis=dict(
    #         title=xaxis_type,
    #         showgrid=True,
    #         gridwidth=0.5,
    #         gridcolor='#444444',
    #         autorange=True,
    #         categoryorder="array",
    #         categoryarray=[x for _, x in sorted(
    #             zip(trace["y"], trace["x"]))]

    #         # ticks="outside",
    #         # tickcolor="#444444",
    #         # ticklen=2,
    #         # zeroline=True,
    #         # zerolinewidth=3,
    #         # zerolinecolor='red',
    #         # titlefont=dict(
    #         #     family='Oswald, sans-serif',
    #         #     size=14,
    #         #     color='lightgrey'
    #         # ),
    #     ),

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
