# import library
import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from scipy import  stats
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import base64
import io

# style of all body
basic_style = {
    "font-size": "9pt",
    "color": "#342B2B",
    "font-family": "Noto Sans JP",
    "min-height": "100vh",
}

# style of tabs
tabs_style = {
    "position": "fixed",
    "top": "56px",
    "padding": "0",
    "height": "100%",
    "width": "200px",
    "overflow-y": "auto",
    "z-index": "1",
    "border-right": "solid 0.5px #AEAAAA",
    "background-color": "#ffffff"
}

# style of tab
tab_style = {
    "width": "184px",
    "border-radius": "8px",
}

# style when tab selected
selected_tab_style = {
    "background-color": "#DBEBF1",
    "color": "#2b4b78",
    "border": "#DBEBF1",
    "font-weight": "bold"
}

# style of contents
contents_style = {
    "position": "relative",
    "padding": "72px 16px 16px 200px",
    "z-index": "0",
}

# instance dash app
app = Dash(
    __name__,
    external_stylesheets = [dbc.themes.FLATLY],
    suppress_callback_exceptions = True,
)

server = app.server

# headers
headers = html.Div(
    [
        # site title
        html.H5(
            'MediSight',
            style = {
                "font-weight": "bold",
                "margin-top": "10px",
                "margin-left": "16px",
                "font-size": "20pt",
                "display": "inline-block"
            }
        ),
        # button of file upload
        dcc.Upload(
            id = "file-select-button",
            children = html.A(
                        "ファイルを選択",
                        style = {
                            "display": "block",
                            'width': '200px',
                            "height": "32px",
                            "border": "solid 1px #AEAAAA",
                            "border-radius": "2px",
                            "text-align": "center",
                            "padding-top": "6px",
                            "cursor": "pointer",
                        }
                    ),
            style = {
                "margin-top": "12px",
                "margin-left": "88px",
                "display": "inline-block"
            }
        ),
        # space of text filename or alert
        html.Div(
            id = "text-filename",
            style = {
                "padding-top": "18px",
                "padding-left": "24px",
                "display": "inline-block"
            }
        ),
    ],
    style = {
        "display": "flex",
        "position": "fixed",
        "top": "0",
        "width": "100%",
        "height": "56px",
        "z-index": "2",
        "border-bottom": "solid 0.5px #AEAAAA",
        "background-color": "#ffffff"
    }
)

# tabs
tabs = html.Div(
    [
        dcc.Tabs(
            id = "tabs-contents-display",
            value = "data-table-tab",
            children=[
                dcc.Tab(
                    label = 'データテーブル',
                    value = 'data-table-tab',
                    style = tab_style,
                    selected_style = selected_tab_style
                ),
                dcc.Tab(
                    label = '1変数の分布',
                    value = 'one-variable-graph-tab',
                    style = tab_style,
                    selected_style = selected_tab_style,
                ),
                dcc.Tab(
                    label = '2変数の分布',
                    value = 'two-variable-graph-tab',
                    style = tab_style,
                    selected_style = selected_tab_style,
                ),
                dcc.Tab(
                    label = '時系列データ',
                    value = 'longitudinal-graph-tab',
                    style = tab_style,
                    selected_style = selected_tab_style,
                ),
            ],
            vertical = True,
            colors={
                "background": "#ffffff",
            },
            style = {
                "margin": "8px"
            }
        ),
    ]
)

# contents
contents = html.Div(
    [
        html.Div(
            id = "data-table-contents-space",
            style = {
                "visibility": "hidden",
                "width": "85%",
                "background-color": "red"
            }
        ),
        html.Div(
            id = "one-variable-graph-contents-space",
            style = {
                "visibility": "hidden",
                "width": "85%",
                "background-color": "red"
            }
        ),
        html.Div(
            id = "two-variable-graph-contents-space",
            style = {
                "visibility": "hidden",
                "width": "85%",
                "background-color": "red"
            }
        ),
        html.Div(
            id = "longitudinal-graph-contents-space",
            style = {
                "visibility": "hidden",
                "width": "85%",
                "background-color": "red"
            }
        ),
    ],
)

# app layout
app.layout = html.Div(
    id = "body-container",
    children = [
        html.Div(
            headers,
        ),
        html.Div(
            [
                html.Div(
                    tabs,
                    style = tabs_style,
                ),
                html.Div(
                    contents,
                    style = contents_style
                )
            ],
            style = {
                "display": "flex"
            }
        ),
    ],
    style = basic_style,
)


# callback when tab select
@callback(
    Output("data-table-contents-space", "style"),
    Output("one-variable-graph-contents-space", "style"),
    Output("two-variable-graph-contents-space", "style"),
    Output("longitudinal-graph-contents-space", "style"),
    Input("tabs-contents-display", "value"),
    State("file-select-button", "contents"),
)
def tab_selected_view(tab, contents):
    # if file selected
    if contents:
        if tab == "data-table-tab":
            return {"visibility": "visible"}, {"visibility": "hidden"}, {"visibility": "hidden"}, {"visibility": "hidden"}
        elif tab == "one-variable-graph-tab":
            return {"visibility": "hidden"}, {"visibility": "visible"}, {"visibility": "hidden"}, {"visibility": "hidden"}
        elif tab == "two-variable-graph-tab":
            return {"visibility": "hidden"}, {"visibility": "hidden"}, {"visibility": "visible"}, {"visibility": "hidden"}
        elif tab == "longitudinal-graph-tab":
            return {"visibility": "hidden"}, {"visibility": "hidden"}, {"visibility": "hidden"}, {"visibility": "visible"}
    # if not file selected
    else:
        return {"visibility": "visible"}, {"visibility": "hidden"}, {"visibility": "hidden"}, {"visibility": "hidden"}


# callback when csv file select
# data table contents space｜view space title and data table
# one variable graph contents space｜view space title and dropdown of select quaritative variable
# two variable graph contents space｜view space title and dropdown of select axis type and variable
# longitudinal graph contents space｜view space title and dropdown of select longitudinal variable
@callback(
    Output("text-filename", "children"),
    Output("data-table-contents-space", "children"),
    Output("one-variable-graph-contents-space", "children"),
    Output("two-variable-graph-contents-space", "children"),
    Output("longitudinal-graph-contents-space", "children"),
    Input("file-select-button", "contents"),
    State("file-select-button", "filename")
)
def data_table_view(contents, filename):
    # text if not file selected
    non_text_select = html.P(
        "※ファイルを選択してください",
        style = {
            "color": "#DC5258"
        }
    )

    # text if file selected
    text_filename = html.P(
        filename
    )

    # if file selected
    if contents:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        # generate the data table
        selected_data_table = html.Div(
            [
                # page title
                html.H2(
                    "データテーブル",
                    style = {
                        "font-size": "16pt",
                        "margin-bottom": "16px"
                    }
                ),
                # table of select data
                html.Div(
                    dash_table.DataTable(
                        id = "table",
                        data = df.to_dict("records"),
                        columns = [
                            {"name": i, "id": i} for i in df.columns
                        ],
                        page_size = 15,
                        style_cell = {
                            "text-align": "center",
                            "max-width": "80px",
                            "min-width": "80px",
                            "white-space": "normal",
                            "border-bottom": "solid 0.5px #AEAAAA"
                        },
                        style_as_list_view = True,
                        style_header = {
                            "background-color": "#ffffff",
                            'font-weight': 'bold',
                            "border-bottom": "solid 1.5px #AEAAAA"
                        },
                        style_table = {
                            "min-width": "100%",
                            'overflowX': 'auto'
                        },
                        sort_action = "native",
                        sort_mode = "multi",
                    ),
                    style = {
                        "border-radius": "2px",
                        "border": "solid 0.5px #AEAAAA",
                        "padding": "40px 24px 24px 24px"
                    }
                )
            ],
            style = {
                "position": "fixed",
                "width": "84%",
                "padding-left": "32px"
            }
        )

        # one variable graph info
        one_variable_graph_info = html.Div(
            [
                html.H2(
                    "1変数の分布",
                    style = {
                        "font-size": "16pt",
                        "margin-bottom": "16px"
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "質的データは",
                            style = {
                                "display": "inline-block",
                                "margin-top": "8px",
                                "margin-right": "16px",
                                "width": "72px"
                            }
                        ),
                        dcc.Dropdown(
                            id = "qualitative-variable",
                            options = [
                                {"value": col, "label": col} for col in df.columns
                            ],
                            multi = True,
                            style = {
                                "display": "inline-block",
                                "width": "640px",
                                "margin-right": "40px"
                            }
                        ),
                        html.Button(
                            '1変数の分布を表示',
                            id = 'one-variable-graph-view',
                            n_clicks = 0,
                            style = {
                                "border": "none",
                                "border-radius": "2px",
                                "text-align": "center",
                                "width": "200px",
                                "height": "32px",
                                "background-color": "#2b4b78",
                                "color": "#ffffff",
                                "display": "inline-block",
                                "margin-top": "2px",
                            }
                        ),
                    ],
                    style = {
                        "display": "flex",
                        "margin-bottom": "16px"
                    }
                ),
                html.Div(
                    id = "one-variable-graph-space",
                )
            ],
            style = {
                "position": "absolute",
                "padding-left": "32px",
            }
        )

        # two variable graph info
        two_variable_graph_info = html.Div(
            [
                html.H2(
                    "2変数の分布",
                    style = {
                        "font-size": "16pt",
                        "margin-bottom": "16px",
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "変数",
                            style = {
                                "display": "inline-block",
                                "margin-top": "8px",
                                "margin-right": "16px",
                                "width": "24px"
                            }
                        ),
                        dcc.Dropdown(
                            id = "axis-variable",
                            options = [
                                {"value": col, "label": col} for col in df.columns
                            ],
                            multi = False,
                            style = {
                                "display": "inline-block",
                                "width": "160px",
                                "margin-right": "8px"
                            }
                        ),
                        html.P(
                            "を",
                            style = {
                                "display": "inline-block",
                                "margin-top": "8px",
                                "margin-right": "8px",
                                "width": "12px"
                            }
                        ),
                        dcc.Dropdown(
                            id = "axis-type",
                            options = [
                                {"value": "xaxis", "label": "説明変数（X軸）"},
                                {"value": "yaxis", "label": "目的変数（Y軸）"}
                            ],
                            multi = False,
                            style = {
                                "display": "inline-block",
                                "width": "160px",
                                "margin-right": "8px"
                            }
                        ),
                        html.P(
                            "に設定",
                            style = {
                                "display": "inline-block",
                                "margin-top": "8px",
                                "margin-right": "40px",
                                "width": "36px"
                            }
                        ),
                        html.Button(
                            '2変数の分布を表示',
                            id = 'two-variable-graph-view',
                            n_clicks = 0,
                            style = {
                                "border": "none",
                                "border-radius": "2px",
                                "text-align": "center",
                                "width": "200px",
                                "height": "32px",
                                "background-color": "#2b4b78",
                                "color": "#ffffff",
                                "display": "inline-block",
                                "margin-top": "2px"
                            }
                        ),
                    ],
                    style = {
                        "display": "flex",
                        "margin-bottom": "16px"
                    }
                ),
                html.Div(
                    id = "two-variable-graph-space"
                )
            ],
            style = {
                "position": "absolute",
                "padding-left": "32px",
            }
        )

        # longitudinal graph info
        longitudinal_graph_info = html.Div(
            [
                html.H2(
                    "時系列データ",
                    style = {
                        "font-size": "16pt",
                        "margin-bottom": "16px"
                    }
                ),
                html.Div(
                    [
                        html.P(
                            "時系列データは",
                            style = {
                                "display": "inline-block",
                                "margin-top": "8px",
                                "margin-right": "16px",
                                "width": "84px"
                            }
                        ),
                        dcc.Dropdown(
                            id = "longitudinal-variable",
                            options = [
                                {"value": col, "label": col} for col in df.columns
                            ],
                            multi = False,
                            style = {
                                "display": "inline-block",
                                "width": "160px",
                                "margin-right": "40px"
                            }
                        ),
                        html.Button(
                            '時系列データを表示',
                            id = 'longitudinal-graph-view',
                            n_clicks = 0,
                            style = {
                                "border": "none",
                                "border-radius": "2px",
                                "text-align": "center",
                                "width": "200px",
                                "height": "32px",
                                "background-color": "#2b4b78",
                                "color": "#ffffff",
                                "display": "inline-block",
                                "margin-top": "2px"
                            }
                        ),
                    ],
                    style = {
                        "display": "flex",
                        "margin-bottom": "16px"
                    }
                ),
                html.Div(
                    id = "longitudinal-graph-space"
                )
            ],
            style = {
                "position": "absolute",
                "padding-left": "32px",
            }
        )

        return text_filename, selected_data_table, one_variable_graph_info, two_variable_graph_info, longitudinal_graph_info
    else:
        return non_text_select, None, None, None, None


# callback when click button of view one variable graph
# one graph contents space | view one variable graph and data info
@callback(
    Output("one-variable-graph-space", "children"),
    Input("one-variable-graph-view", "n_clicks"),
    State("qualitative-variable", "value"),
    State("file-select-button", "contents"),
)
def view_one_variable_graph(n_clicks, qualitative_variable, contents):
    if n_clicks:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        
        histograms = []

        for col in df.columns:
            df_sorted = df.sort_values(
                by = col,
                ascending = True
            )
            # 質的データの場合
            if col in qualitative_variable:
                hist_fig = px.histogram(
                    df_sorted,
                    x = col,
                    nbins = 24,
                    color_discrete_sequence = ["#2b4b78"],
                )

                hist_fig.update_layout(
                    paper_bgcolor = '#ffffff',
                    plot_bgcolor = '#ffffff',
                )

                # X軸とY軸の線を設定
                hist_fig.update_xaxes(
                    showline = True,
                    linewidth = 0.5,
                   linecolor = '#AEAAAA'
                )
                hist_fig.update_yaxes(
                    showline = True,
                    linewidth = 0.5,
                   linecolor = '#AEAAAA'
                )

                # 質的データの度数、相対度数、累積相対度数を計算
                value_counts = df[col].value_counts()
                relative_freq = df[col].value_counts(normalize = True).round(2)
                cumulative_freq = df[col].value_counts(normalize = True).cumsum().round(2)

                # データをDashのDataTableに整形
                table_data = pd.DataFrame({
                    col: value_counts.index,
                    '度数': value_counts.values,
                    '相対度数': relative_freq.values,
                    '累積相対度数': cumulative_freq.values
                })

                # DashのDataTableコンポーネントを作成
                data_table = dash_table.DataTable(
                    data = table_data.to_dict('records'),
                    columns = [{'name': i, 'id': i} for i in table_data.columns],
                    page_size = 10,
                    style_cell = {
                        "text-align": "center",
                        "max-width": "80px",
                        "min-width": "80px",
                        "white-space": "normal",
                        "border-bottom": "solid 0.5px #AEAAAA"
                    },
                    style_as_list_view = True,
                    style_header = {
                        "background-color": "#ffffff",
                        'font-weight': 'bold',
                        "border-bottom": "solid 1.5px #AEAAAA"
                    },
                    style_table = {
                        "min-width": "100%",
                        'overflowX': 'auto'
                    },
                )

                histograms.append(
                    html.Div(
                        [
                            html.Div(
                                html.H3(
                                    "{}の分布と度数分布表".format(col),
                                    style = {
                                        "font-size": "12pt",
                                        "margin": "16px 0px 0px 40px"
                                    }
                                )
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            figure = hist_fig
                                        ),
                                        style = {
                                            "width": "50%",
                                            "display": "inline-block",
                                            "margin": "8px",
                                        }
                                    ),
                                    html.Div(
                                        data_table,
                                        style = {
                                            "width": "50%",
                                            "display": "inline-block",
                                            "margin": "40px 8px 8px 8px"
                                        }
                                    )
                                ],
                                style = {
                                    "display": "flex"
                                }
                            )
                            
                        ],
                        style = {
                            "border-radius": "2px",
                            "border": "solid 0.5px #AEAAAA",
                            "margin": "0px 16px 16px 0px",
                            "width": "1200px",
                            "height": "520px"
                        }
                    )
                )
                
            # 量的データの場合
            else:
                hist_fig = px.histogram(
                    df_sorted,
                    x = col,
                    nbins = 24,
                    color_discrete_sequence = ["#2b4b78"]
                )

                hist_fig.update_layout(
                    paper_bgcolor = '#ffffff',
                    plot_bgcolor = '#ffffff'
                )

                # X軸とY軸の線を設定
                hist_fig.update_xaxes(
                    showline = True,
                    linewidth = 0.5,
                   linecolor = '#AEAAAA'
                )
                hist_fig.update_yaxes(
                    showline = True,
                    linewidth = 0.5,
                   linecolor = '#AEAAAA'
                )

                # 量的データの基本統計量を計算
                stats_data = {
                    "基本統計量": ["平均", "中央値", "最頻値", "最大値", "最小値", "標準偏差", "歪度", "尖度", "25％四分位点", "50％四分位点", "75％四分位点"],
                    "値": [
                        "{:.2f}".format(np.mean(df[col])),
                        "{:.2f}".format(np.median(df[col])),
                        "{}".format(stats.mode(df[col])[0]),
                        "{:.2f}".format(np.max(df[col])),
                        "{:.2f}".format(np.min(df[col])),
                        "{:.2f}".format(np.std(df[col], ddof=1)),
                        "{:.2f}".format(stats.skew(df[col])),
                        "{:.2f}".format(stats.kurtosis(df[col])),
                        "{:.2f}".format(np.percentile(df[col], 25)),
                        "{:.2f}".format(np.percentile(df[col], 50)),
                        "{:.2f}".format(np.percentile(df[col], 75))
                    ]
                }
                stats_df = pd.DataFrame(stats_data)

                # DashのDataTableコンポーネントを作成
                stats_table = dash_table.DataTable(
                    data = stats_df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in stats_df.columns],
                    style_cell = {
                        "text-align": "center",
                        "max-width": "80px",
                        "min-width": "80px",
                        "white-space": "normal",
                        "border-bottom": "solid 0.5px #AEAAAA"
                    },
                    style_as_list_view = True,
                    style_header = {
                        "background-color": "#ffffff",
                        'font-weight': 'bold',
                        "border-bottom": "solid 1.5px #AEAAAA"
                    },
                    style_table = {
                        "min-width": "100%",
                        'overflowX': 'auto'
                    },
                )

                histograms.append(
                    html.Div(
                        [
                            html.Div(
                                html.H3(
                                    "{}の分布と基本統計量".format(col),
                                    style = {
                                        "font-size": "12pt",
                                        "margin": "16px 0px 0px 40px"
                                    }
                                )
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            figure = hist_fig
                                        ),
                                        style = {
                                            "width": "50%",
                                            "display": "inline-block",
                                            "margin": "8px"
                                        }
                                    ),
                                    html.Div(
                                        stats_table,
                                        style = {
                                            "width": "50%",
                                            "display": "inline-block",
                                            "margin": "40px 8px 8px 8px",
                                        }
                                    )
                                ],
                                style = {
                                    "display": "flex"
                                }
                            ) 
                        ],
                        style = {
                            "border-radius": "2px",
                            "border": "solid 0.5px #AEAAAA",
                            "margin": "0px 16px 16px 0px",
                            "width": "1200px",
                            "height": "520px"
                        }
                    )
                )

        # Wrapping histgrams in a row div
        histograms_layout = html.Div(
            histograms,
        )

        return histograms_layout


# callback when click button of view two variable graph
# two graph contents space｜view two variable graph
@callback(
    Output("two-variable-graph-space", "children"),
    Input("two-variable-graph-view", "n_clicks"),
    State("file-select-button", "contents"),
    State("axis-variable", "value"),
    State("axis-type", "value")
)
def view_two_variable_graph(n_clicks, contents, axis_variable, axis_type):
    if n_clicks:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        scatters = []

        if axis_type == "xaxis":
            for col in df.columns:
                if col != axis_variable:
                    df_sorted = df.sort_values(
                        by = axis_variable,
                        ascending = True
                    )

                    scat_fig = px.scatter(
                        df_sorted,
                        x = axis_variable,
                        y = col
                    )

                    scat_fig.update_layout(
                        paper_bgcolor = '#ffffff',
                        plot_bgcolor = '#ffffff'
                    )

                    # X軸とY軸の線を設定
                    scat_fig.update_xaxes(
                        showline = True,
                        linewidth = 0.5,
                    linecolor = '#AEAAAA'
                    )
                    scat_fig.update_yaxes(
                        showline = True,
                        linewidth = 0.5,
                    linecolor = '#AEAAAA'
                    )

                    # 散布図のマーカーの色を設定
                    scat_fig.update_traces(
                        marker = dict(
                            color = "#2b4b78",
                            size = 4
                        ) # ここで色とサイズを設定
                    )

                    scatters.append(
                        html.Div(
                            [
                                html.Div(
                                    html.H3(
                                        "{}（X軸）と{}（Y軸）の分布".format(axis_variable, col),
                                        style = {
                                            "font-size": "12pt",
                                            "margin": "16px 0px 0px 40px"
                                        }
                                    )
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            dcc.Graph(
                                                figure = scat_fig
                                            ),
                                            style = {
                                                "width": "96%",
                                                "margin": "8px"
                                            }
                                        ),
                                    ]
                                ) 
                            ],
                            style = {
                                "border-radius": "2px",
                                "border": "solid 0.5px #AEAAAA",
                                "margin": "0px 2px 16px 0px",
                                "width": "1200px",
                                "height": "520px"
                            }
                        )
                    )
        
        elif axis_type == "yaxis":
            for col in df.columns:
                if col != axis_variable:
                    df_sorted = df.sort_values(
                        by = col,
                        ascending = True
                    )
                    
                    scat_fig = px.scatter(
                        df_sorted,
                        x = col,
                        y = axis_variable
                    )

                    # グラフの背景色と線の色を設定
                    scat_fig.update_layout(
                        paper_bgcolor = '#ffffff',
                        plot_bgcolor = '#ffffff'
                    )

                    # X軸とY軸の線を設定
                    scat_fig.update_xaxes(
                        showline = True,
                        linewidth = 0.5,
                    linecolor = '#AEAAAA'
                    )
                    scat_fig.update_yaxes(
                        showline = True,
                        linewidth = 0.5,
                    linecolor = '#AEAAAA'
                    )

                    # 散布図のマーカーの色を設定
                    scat_fig.update_traces(
                        marker = dict(
                            color = "#2b4b78",
                            size = 4
                        ) # ここで色とサイズを設定
                    )

                    scatters.append(
                        html.Div(
                            [
                                html.Div(
                                    html.H3(
                                        "{}（X軸）と{}（Y軸）の分布".format(col, axis_variable),
                                        style = {
                                            "font-size": "12pt",
                                            "margin": "16px 0px 0px 40px"
                                        }
                                    )
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            dcc.Graph(
                                                figure = scat_fig
                                            ),
                                            style = {
                                                "width": "96%",
                                                "margin": "8px"
                                            }
                                        ),
                                    ]
                                ) 
                            ],
                            style = {
                                "border-radius": "2px",
                                "border": "solid 0.5px #AEAAAA",
                                "margin": "0px 2px 16px 0px",
                                "width": "1200px",
                                "height": "520px"
                            }
                        )
                    )

        scatters_layout = html.Div(
            scatters,
        )
            
        return scatters_layout


# callback when click button of view longitudinal graph
# longitudinal graph contents space｜view longitudinal graph
@callback(
    Output("longitudinal-graph-space", "children"),
    Input("longitudinal-graph-view", "n_clicks"),
    State("longitudinal-variable", "value"),
    State("file-select-button", "contents")
)
def view_longitudinal_graph(n_clicks, longitudinal_variable, contents):
    if n_clicks:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

        df_sorted = df.sort_values(
            by = longitudinal_variable,
            ascending = True
        )

        line_scatters = []

        for col in df_sorted.columns:
            if col != longitudinal_variable:
                line_scatter = px.line(
                    df_sorted,
                    x = longitudinal_variable,
                    y = col,
                )

                # グラフの背景色と線の色を設定
                line_scatter.update_layout(
                    paper_bgcolor = '#ffffff',
                    plot_bgcolor = '#ffffff'
                )

                # X軸とY軸の線を設定
                line_scatter.update_xaxes(
                    showline = True,
                    linewidth = 0.5,
                linecolor = '#AEAAAA'
                )
                line_scatter.update_yaxes(
                    showline = True,
                    linewidth = 0.5,
                linecolor = '#AEAAAA'
                )

                line_scatter.update_traces(
                    line = dict(color = "#2b4b78")
                )

                line_scatters.append(
                    html.Div(
                        [
                            html.Div(
                                html.H3(
                                    "{}の時系列データ".format(col),
                                    style = {
                                        "font-size": "12pt",
                                        "margin": "16px 0px 0px 40px"
                                    }
                                )
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            figure = line_scatter
                                        ),
                                        style = {
                                            "width": "96%",
                                            "margin": "8px"
                                        }
                                    ),
                                ]
                            ) 
                        ],
                        style = {
                            "border-radius": "2px",
                            "border": "solid 0.5px #AEAAAA",
                            "margin": "0px 2px 16px 0px",
                            "width": "1200px",
                            "height": "520px"
                        }
                    )
                )
        
        line_scatters_layout = html.Div(
            line_scatters,
        )
            
        return line_scatters_layout


# app start
if __name__ == "__main__":
    app.run(port=10000, debug=False)
