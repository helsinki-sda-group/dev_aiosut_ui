from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.constants import (
    SEASONS,
    WEEKDAYS,
    MOBILITY_DEMAND,
    AREAS,
    TIMELINE_FUNCTIONS,
    OBJECTIVES,
    OPTIMIZATION_SLIDER_MARKS,
    SITUATIONS,
    TRAFFIC_VARIABLES,
    TIMESTEPS,
)

basic_style = {"paddingTop": "2vh", "paddingBottom": "2vh"}
empty_style = {"display": "none"}
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]


def _optimization_row(objective, icon_class):
    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.I(
                            className=icon_class,
                            style={"paddingRight": "2em", "fontSize": "1.5em"},
                        ),
                        html.Label(
                            objective,
                            style={"fontSize": "1.2em"},
                            htmlFor=f"{objective.lower()}-priority",
                        ),
                    ]
                ),
                width={"size": 3},
            ),
            dbc.Col(
                html.Div(
                    [
                        dcc.Slider(
                            step=None,
                            marks={
                                i: {
                                    "label": f"{OPTIMIZATION_SLIDER_MARKS[i]}",
                                    "style": {"fontSize": "1.2em"},
                                }
                                for i in range(len(OPTIMIZATION_SLIDER_MARKS))
                            },
                            value=0,
                            id=f"{objective.lower()}-priority",
                            disabled=True,
                        ),
                    ]
                ),
            ),
        ],
        style={
            "fontSize": "1.1em",
            "paddingBottom": "2vh",
            "paddingTop": "2vh",
            "width": "75vw",
        },
        align="center",
        justify="center",
    )


plots_location_text = html.Div(
    "Location: Network",
    id="location-text",
    style={
        "fontSize": "1.2em",
        "paddingBottom": "4vh",
        "display": "block",
        "paddingTop": "2vh",
    },
)

plots_reset_button = dbc.Button(
    "Reset location",
    id="reset-location-button",
    n_clicks=0,
    style={
        "display": "block",
        "fontSize": "1em",
        "automargin": True,
        "padding": "1vh",
    },
)


project_heading_col = dbc.Col(
    html.Div(
        [
            html.H1(
                "AI-based optimisation tool for sustainable urban planning (AIOSut)"
            ),
        ]
    ),
)

project_info_button_col = dbc.Col(
    html.Div(
        [
            dbc.Button(
                "Say what?",
                id="project-info-button",
                className="mb-3 d-md-block",
                color="secondary",
                n_clicks=0,
                style={"float": "right"},
            ),
        ]
    )
)

project_header_row = dbc.Row(
    [
        project_heading_col,
        project_info_button_col,
    ],
    align="center",
    style={"paddingBottom": "1vh"},
)

project_info_collapse = dbc.Collapse(
    dbc.Card(
        dbc.CardBody(
            dcc.Markdown(
                """
                **AIOSut** is a Proof of Concept -project funded by the Research Council of Finland. The project's aim is to develop a prototype tool that utilizes AI-based scalable and generalisable models for urban planning optimization and features a visual interface that makes the use of the models and analysing of the results easy, without requiring AI knowledge from the user.
                
                [GitHub page](https://github.com/helsinki-sda-group/dev_aiosut_ui)""",
                link_target="_blank",
            ),
        ),
    ),
    id="project-info-collapse",
    is_open=False,
    style={"paddingTop": "2vh", "paddingBottom": "3vh", "width": "auto"},
)

simulation_time_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-calendar-day",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Time of week",
                htmlFor="crossfilter-time",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=WEEKDAYS,
                value=WEEKDAYS[0]["value"],
                # placeholder="Select time of week...",
                id="crossfilter-time",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
    )
)

simulation_demand_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-graph-up",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Demand",
                htmlFor="crossfilter-demand",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=MOBILITY_DEMAND,
                value=MOBILITY_DEMAND[1]["value"],
                # placeholder="Select demand...",
                id="crossfilter-demand",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
    )
)

simulation_area_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-map",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Area",
                htmlFor="crossfilter-area",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=AREAS,
                # placeholder="Select area...",
                value=AREAS[2]["value"],
                id="crossfilter-area",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
    )
)

simulation_season_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-cloud-sun",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Season",
                htmlFor="crossfilter-season",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=SEASONS,
                # placeholder="Select season...",
                value=SEASONS[2]["value"],
                id="crossfilter-season",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
    ),
)

scenario_parameter_row = html.Div(
    dbc.Row(
        [
            simulation_season_col,
            simulation_time_col,
            simulation_area_col,
            simulation_demand_col,
        ],
    ),
    style=basic_style,
)

simulation_heading_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-gear",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
            ),
            html.H2("Simulation parameters"),
        ]
    ),
)

simulation_info_button_col = dbc.Col(
    html.Div(
        dbc.Button(
            "What do these do?",
            id="scenario-info-button",
            className="mb-3 d-md-block",
            color="secondary",
            n_clicks=0,
            style={"float": "right"},
        ),
    )
)

simulation_header_row = dbc.Row(
    [
        simulation_heading_col,
        simulation_info_button_col,
    ],
    align="center",
    style={"paddingBottom": "1vh"},
)

simulation_info_collapse = dbc.Collapse(
    dbc.Card(
        dbc.CardBody(
            dcc.Markdown(
                """
                            These build your very own simulated city ("scenario" for short)!

                            * *Season* controls the weather conditions - keeping the winters cool and summers hot! Bikers love it.
                            * *Time of week* refers to what day should be simulated. *Weekday* means it is time to hurry to work between Monday and Friday and *Weekend* is for that relaxed sightseeing on Saturday or Sunday.
                            * *Area* changes what area is being simulated. Trying to take it all in all at once made our head spin (the AI's too), so we made a tour around the city instead.
                            * *Demand* decides how much mobility is going on. *Regular* projection refers to what one would expect to see based on the historical data; *Low* scales the regular projection down by 20%, while *High* increases it by 20%.
                            * *Priority* refers to how important the objective is for you. It helps the AI when it is comparing apples into oranges: you need more apples from the higher priority objective for it to be equal to the lower priority objective's orange.
                            """,
                link_target="_blank",
            ),
        ),
    ),
    id="scenario-info-collapse",
    is_open=False,
    style={"paddingTop": "2vh", "paddingBottom": "3vh", "width": "auto"},
)

simulation_button = html.Div(
    [
        html.Center(
            dbc.Button(
                html.Label(
                    "Simulate",
                    style={"fontSize": 18},
                    htmlFor="simulate-button",
                ),
                size="lg",
                id="simulate-button",
                n_clicks=0,
                disabled=True,
            ),
            style={
                "paddingTop": "3vh",
                "paddingBottom": "3vh",
                "display": "block",
            },
        ),
    ],
    style=basic_style,
)

optimization_header = html.Div(
    [
        html.I(
            className="bi bi-sort-up",
            style={
                "paddingRight": "20px",
                "fontSize": "1.75em",
                "float": "left",
                "decorative": True,
            },
        ),
        html.P(
            "Priorities",
            style={
                "fontSize": "1.4em",
            },
        ),
    ],
    style=basic_style,
)

optimization_sliders = html.Div(
    [
        _optimization_row(
            objective=OBJECTIVES[1],
            icon_class="bi bi-car-front-fill",
        ),
        _optimization_row(
            objective=OBJECTIVES[2],
            icon_class="bi bi-wind",
        ),
        _optimization_row(
            objective=OBJECTIVES[3],
            icon_class="bi bi-house-heart-fill",
        ),
    ],
)

results_heading_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-bar-chart-line",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
            ),
            html.H2("Results"),
        ]
    ),
)

results_info_button_col = dbc.Col(
    html.Div(
        dbc.Button(
            "Explain, please!",
            id="results-info-button",
            className="mb-3 d-md-block",
            color="secondary",
            n_clicks=0,
            style={"float": "right"},
        ),
    )
)

results_info_collapse = html.Div(
    [
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown(
                        """
                            There is a lot going on in the city - a bit too much, which is why we brought you tabs. *Summary* lets you see the big picture "before" (*Baseline*) and "after" (*Optimized*) the AI renovation, while the other tabs – *Traffic*, *Air quality* and *Livability* – zoom in one objective and different variables related to that objective.
                            """,
                        link_target="_blank",
                    ),
                ),
            ),
            id="results-info-collapse",
            is_open=False,
            style={"paddingTop": "2vh", "paddingBottom": "3vh", "width": "auto"},
        ),
    ],
)


results_tabs = html.Div(
    [
        dcc.Tabs(
            id="results-tabs",
            children=[
                # Summary
                dcc.Tab(
                    label=f"\t{OBJECTIVES[0]}",
                    value=OBJECTIVES[0],
                    className="bi bi-card-list",
                    style={
                        "fontSize": "1em",
                        "decorative": True,
                        "margin": "auto",
                    },
                ),
                # Traffic
                dcc.Tab(
                    label=f"\t{OBJECTIVES[1]}",
                    value=OBJECTIVES[1],
                    className="bi bi-car-front-fill",
                    style={
                        "fontSize": "1em",
                        "decorative": True,
                    },
                ),
                # AQ
                dcc.Tab(
                    label=f"\t{OBJECTIVES[2]}",
                    value=OBJECTIVES[2],
                    className="bi bi-wind",
                    style={
                        "fontSize": "1em",
                        "decorative": True,
                    },
                ),
                # Livability
                dcc.Tab(
                    label=f"\t{OBJECTIVES[3]}",
                    value=OBJECTIVES[3],
                    className="bi bi-house-heart-fill",
                    style={
                        "fontSize": "1em",
                        "decorative": True,
                    },
                ),
            ],
        ),
    ],
    style=basic_style,
)

viz_heading_col = dbc.Col(
    html.Div(
        [
            html.I(
                className="bi bi-filter",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
            ),
            html.H3("Filters"),
        ]
    ),
)

viz_info_button_col = dbc.Col(
    html.Div(
        dbc.Button(
            "Hold on a minute!",
            id="filter-info-button",
            className="mb-3 d-md-block",
            color="secondary",
            n_clicks=0,
            style={"float": "right"},
        ),
    )
)

viz_info_collapse = html.Div(
    [
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown(
                        """
                    When you get your BIG dataset back, not every second needs to be recorded there as is, right?
                    * *Situation* lets you see how things were in the city "before" (*Baseline*) and "after" (*Optimized*) the AI renovation.
                    * *Variable* filters the distractions out and shows you one variable at a time.
                    * *Temporal resolution* adjusts how detailed visualizations are in the time axis. By default, every minute is displayed, resulting in 60 data points out of one hour. For example, "Every quarter", in the other hand, would display every 15 minutes as one data point, resulting in four data points in one hour.
                    * *Temporal aggregation* defines the method how each second of raw simulation data is mapped for a given temporal resolution. "Sum" just sums everything&#42 together, while "Average" takes the mean of everything&#42. For example, with three seconds' worth of some data: "Sum": `[1,2,3] -> 6`; "Average": `[1,2,3] -> 2`.
                    
                    &#42Well, everything except for average values, Speed and Noise as we can't provide speed of light -travelling or hearing aids here, sorry! Instead, Speed gets averaged always, Noise has its own formula called Harmonoise and averages will always be averages.
                    """,
                        link_target="_blank",
                    ),
                ),
            ),
            id="filter-info-collapse",
            is_open=False,
            style={
                "paddingTop": "2vh",
                "paddingBottom": "3vh",
                "width": "auto",
            },
        ),
    ]
)

viz_temporal_resolution_col = dbc.Col(
    # Temporal aggregation
    html.Div(
        [
            html.I(
                className="bi bi-stack",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Temporal aggregation",
                htmlFor="crossfilter-timeline-type",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=TIMELINE_FUNCTIONS,
                placeholder="Select function...",
                id="crossfilter-timeline-type",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
        style=empty_style,
        id="timeline-div",
    ),
)

viz_timestep_interval_col = dbc.Col(
    # Timestep interval
    html.Div(
        [
            html.I(
                className="bi bi-clock",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Temporal resolution",
                htmlFor="crossfilter-timestep",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=TIMESTEPS,
                placeholder="Select resolution...",
                id="crossfilter-timestep",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
        style=empty_style,
        id="timestep-div",
    ),
)

viz_variable_col = dbc.Col(
    # Variable dropdown
    html.Div(
        [
            html.I(
                className="bi bi-search",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Variable",
                htmlFor="crossfilter-variable",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=TRAFFIC_VARIABLES,
                placeholder="Select variable...",
                id="crossfilter-variable",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
        style=empty_style,
        id="variable-div",
    ),
)

viz_situation_col = dbc.Col(
    # Situation dropdown
    html.Div(
        [
            html.I(
                className="bi bi-check-circle",
                style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "decorative": True,
                },
            ),
            html.Label(
                "Situation",
                htmlFor="crossfilter-situation",
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
            dcc.Dropdown(
                options=SITUATIONS,
                placeholder="Select situation...",
                id="crossfilter-situation",
                optionHeight=50,
                style={"fontSize": "1.1em"},
            ),
        ],
        style=empty_style,
        id="situation-div",
    ),
)

viz_full_parameter_row = dbc.Row(
    [
        viz_situation_col,
        viz_variable_col,
        viz_timestep_interval_col,
        viz_temporal_resolution_col,
    ],
    align="top",
)

viz_header_row = dbc.Row(
    [
        viz_heading_col,
        viz_info_button_col,
    ],
    align="top",
    style={"paddingBottom": "1vh"},
)


def _project_section():
    return html.Div(
        [
            project_header_row,
            project_info_collapse,
            html.Hr(),
        ],
        style=basic_style,
    )


def _simulation_parameters_section():
    return html.Div(
        [
            simulation_header_row,
            simulation_info_collapse,
            scenario_parameter_row,
            optimization_header,
            optimization_sliders,
            simulation_button,
            html.Hr(),
        ],
        style=basic_style,
    )


def _results_section():
    return html.Div(
        [
            html.Div(
                [
                    dbc.Row(
                        [
                            results_heading_col,
                            results_info_button_col,
                        ],
                        align="center",
                        style={"paddingBottom": "1vh"},
                    ),
                ],
            ),
            results_info_collapse,
            results_tabs,
        ],
        style=basic_style,
    )


def _viz_parameters_section():
    return html.Div(
        [
            viz_header_row,
            viz_info_collapse,
            html.Div(
                viz_full_parameter_row,
                id="viz-parameter-row",
                style=basic_style,
            ),
            html.Center(
                dbc.Button(
                    "Visualize",
                    id="visualize-button",
                    className="mb-3 d-md-block",
                    color="primary",
                    n_clicks=0,
                    style={"fontSize": "1.2em"},
                ),
                style={"paddingTop": "4vh", "paddingBottom": "3vh"},
            ),
        ],
        id="viz-div",
        style=basic_style,
    )


def _plots_section():
    return html.Div(
        [
            html.Center(
                [
                    # Summary actions
                    html.Div(
                        [],
                        id="summary-text",
                    ),
                    # First graph
                    html.Div(
                        [],
                        id="figure-one-div",
                    ),
                    # Second graph
                    html.Div(
                        [],
                        id="figure-two-div",
                    ),
                    # Third graph
                    html.Div(
                        [],
                        id="figure-three-div",
                    ),
                    # Fourth graph
                    html.Div(
                        [],
                        id="figure-four-div",
                    ),
                ]
            ),
        ],
        id="plots-div",
        style=basic_style,
    )


def app_layout():
    return html.Div(
        [
            _project_section(),
            _simulation_parameters_section(),
            _results_section(),
            _viz_parameters_section(),
            dcc.Loading(
                overlay_style={
                    "visibility": "visible",
                    "filter": "blur(2px)",
                },
                style={"paddingTop": "5vh", "paddingBottom": "2vh"},
                type="circle",
                delay_hide=1000,
                children=_plots_section(),
            ),
        ],
        id="app-div",
        style={
            "width": "98vw",
            "automargin": True,
            "paddingLeft": "2vw",
            "paddingRight": "2vw",
            "paddingTop": "3vh",
            "paddingBottom": "3vh",
        },
    )
