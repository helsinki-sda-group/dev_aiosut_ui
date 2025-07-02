from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
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
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]


def optimization_row(objective, icon_class):
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
                id=f"{objective}-col-1",
                align="center",
                width={"size": 3},
            ),
            dbc.Col(
                html.Div(
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
                    ),
                ),
                id=f"{objective}-col-2",
                align="center",
            ),
        ],
        style={
            "fontSize": 18,
            "paddingBottom": "2vh",
            "paddingTop": "2vh",
            "width": "75vw",
        },
        align="center",
        justify="start",
    )


def collapse(id, text):
    return html.Div(
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown(
                        text,
                        link_target="_blank",
                    ),
                ),
            ),
            id=id,
            is_open=False,
            style={"paddingTop": "2vh", "paddingBottom": "3vh", "width": "auto"},
        ),
    )


def info_button(label, id):
    return (
        dbc.Button(
            label,
            id=id,
            className="mb-3 d-md-block",
            color="secondary",
            n_clicks=0,
            style={"float": "right"},
        ),
    )


def header_and_info_button_row(
    header,
    button_label,
    button_id,
    icon_class=None,
    icon_style=None,
):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.I(
                                    className=icon_class,
                                    style=icon_style,
                                ),
                                header,
                            ]
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            info_button(button_label, button_id),
                        )
                    ),
                ],
                align="center",
                style={"paddingBottom": "1vh"},
            ),
        ],
        id=f"{button_id}-div",
    )


def dropdown(
    options,
    id,
    dropdown_style={"margin": "auto", "textAlign": "left"},
    style={"font-size": "1.1em", "width": True},
):
    return html.Div(
        dcc.Dropdown(
            options=options,
            placeholder="Select...",
            id=id,
            optionHeight=50,
            style=dropdown_style,
        ),
        style=style,
        id=f"{id}-div",
    )


def icon_and_label(
    label,
    html_for,
    icon_class=None,
    icon_style=None,
):
    return html.Div(
        [
            html.I(
                className=icon_class,
                style=icon_style,
            ),
            html.Label(
                label,
                htmlFor=html_for,
                style={
                    "fontSize": "1.4em",
                    "paddingBottom": "2vh",
                    "paddingTop": "1vh",
                },
            ),
        ],
        style=basic_style,
        id=f"{html_for}-iconlabel-div",
    )


def _viz_parameter_row():
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    # Situation buttons
                    html.Div(
                        [
                            icon_and_label(
                                label="Situation",
                                html_for="crossfilter-situation",
                                icon_class="bi bi-check-circle",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=SITUATIONS,
                                id="crossfilter-situation",
                                style={"font-size": "1.1em"},
                            ),
                        ],
                        id="situation-div",
                        style={"display": "none"},
                    ),
                    id="situation-col",
                ),
                dbc.Col(
                    # Variable dropdown
                    html.Div(
                        [
                            icon_and_label(
                                label="Variable",
                                html_for="crossfilter-variable",
                                icon_class="bi bi-search",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=TRAFFIC_VARIABLES,
                                id="crossfilter-variable",
                                style={"font-size": "1.1em"},
                            ),
                        ],
                        id="variable-div",
                        style={"display": "none"},
                    ),
                ),
                dbc.Col(
                    # Timestep interval
                    html.Div(
                        [
                            icon_and_label(
                                label="Temporal resolution",
                                html_for="crossfilter-timestep",
                                icon_class="bi bi-clock",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=TIMESTEPS,
                                id="crossfilter-timestep",
                                style={"font-size": "1.1em"},
                            ),
                        ],
                        id="timestep-div",
                        style={"display": "none"},
                    ),
                ),
                dbc.Col(
                    # Temporal aggregation
                    html.Div(
                        [
                            icon_and_label(
                                label="Temporal aggregation",
                                html_for="crossfilter-timeline-type",
                                icon_class="bi bi-stack",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=TIMELINE_FUNCTIONS,
                                id="crossfilter-timeline-type",
                                style={"font-size": "1.1em"},
                            ),
                        ],
                        id="timeline-div",
                        style={"display": "none"},
                    ),
                ),
            ],
            align="top",
        ),
        id="viz-params",
    )


# Visualization parameters
def viz_params():
    return html.Div(
        [
            html.Div(
                header_and_info_button_row(
                    header=html.H3("Filters"),
                    button_label="Hold on a minute!",
                    button_id="filter-info-button",
                    icon_class="bi bi-filter",
                    icon_style={
                        "paddingRight": "20px",
                        "fontSize": "1.75em",
                        "float": "left",
                        "decorative": True,
                    },
                ),
            ),
            collapse(
                id="filter-info-collapse",
                text="""
                    When you get your BIG dataset back, not every second needs to be recorded there as is, right?
                    * *Situation* lets you see how things were in the city "before" (*Baseline*) and "after" (*Optimized*) the AI renovation.
                    * *Variable* filters the distractions out and shows you one variable at a time.
                    * *Resolution* adjusts how many seconds are displayed as one temporal data point in graphs. By default, every minute is displayed, resulting in 60 data points out of one hour. For example, "Every quarter", in the other hand, would display every 15 minutes as one data point, resulting in four data points in one hour.
                    * *Temporal aggregation* defines the method how each second of data is mapped in given resolution. "Sum" just sums everything&#42 together, while "Average" takes the mean of everything&#42. For example, with three seconds of some data points: "Sum": `[1,2,3] -> 6`; "Average": `[1,2,3] -> 2`.
                    
                    &#42Well, everything except for average values, Speed and Noise as we can't provide speed of light -travelling or hearing aids here, sorry! Instead, Speed gets averaged always, Noise has its own formula called Harmonoise and averages will always be averages.
                    """,
            ),
            _viz_parameter_row(),
        ],
        id="viz-div",
        style={"display": "none"},
    )


def plot_results():
    return html.Center(
        html.Div(
            [
                # Summary actions
                html.Div(
                    dcc.Markdown(
                        "",
                        id="summary-text",
                    ),
                    id=f"summary-text-div",
                    style={"display": "none"},
                ),
                # Heatmap div
                html.Div(
                    [
                        # Figure
                        dcc.Loading(
                            dcc.Graph(
                                id="figure-one",
                                responsive=True,
                                config={"showTips": True},
                                style={
                                    "height": "45vw",
                                    "width": "68vw",
                                    "display": "block",
                                },
                            ),
                            type="cube",
                        ),
                        # Location text
                        html.P(
                            "",
                            id="location-text",
                            style={
                                "fontSize": "1em",
                                "paddingBottom": "4vh",
                                "display": "block",
                                "paddingTop": "2vh",
                            },
                        ),
                        # Reset button
                        dbc.Button(
                            "Reset location",
                            id="reset-location-button",
                            n_clicks=0,
                            style={
                                "display": "block",
                                "font-size": "0.75em",
                                "automargin": True,
                                "padding": "1vh",
                            },
                        ),
                    ],
                    id="figure-one-div",
                    style={"display": "none"},
                ),
                # Second graph
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id="figure-two",
                            responsive=True,
                            style={"height": "30vw"},
                        ),
                        type="cube",
                    ),
                    id="figure-two-div",
                    style=basic_style,
                ),
                # Third graph
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id="figure-three",
                            responsive=True,
                            style={"height": "30vw"},
                        ),
                        type="cube",
                    ),
                    id="figure-three-div",
                    style={"display": "none"},
                ),
                # Fourth graph
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id="figure-four",
                            responsive=True,
                            style={"height": "30vw"},
                        ),
                        type="cube",
                    ),
                    id="figure-four-div",
                    style={"display": "none"},
                ),
            ],
            id="plots-div",
            style={"display": "none"},
        ),
    )


def project_info():
    """Renders the project info section."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H1(
                    "AI-based optimisation tool for sustainable urban planning (AIOSut)",
                ),
                button_label="Say what?",
                button_id="project-info-button",
            ),
            collapse(
                id="project-info-collapse",
                text="""
                **AIOSut** is a Proof of Concept -project funded by the Research Council of Finland. The project's aim is to develop a prototype tool that utilizes AI-based scalable and generalisable models for urban planning optimization and features a visual interface that makes the use of the models and analysing of the results easy, without requiring AI knowledge from the user.
                
                [GitHub page](https://github.com/helsinki-sda-group/dev_aiosut_ui)""",
            ),
            html.Hr(),
        ],
        id="project-info-div",
        style=basic_style,
    )


def _scenario_parameter_row():
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            icon_and_label(
                                label="Season",
                                html_for="crossfilter-season",
                                icon_class="bi bi-cloud-sun",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=SEASONS,
                                id="crossfilter-season",
                            ),
                        ],
                        id="season-col",
                    ),
                ),
                dbc.Col(
                    html.Div(
                        [
                            icon_and_label(
                                label="Time of week",
                                html_for="crossfilter-time",
                                icon_class="bi bi-calendar-day",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=WEEKDAYS,
                                id="crossfilter-time",
                            ),
                        ],
                        id="time-col",
                    )
                ),
                dbc.Col(
                    html.Div(
                        [
                            icon_and_label(
                                label="Area",
                                html_for="crossfilter-area",
                                icon_class="bi bi-geo-alt",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=AREAS,
                                id="crossfilter-area",
                            ),
                        ],
                        id="area-col",
                    )
                ),
                dbc.Col(
                    html.Div(
                        [
                            icon_and_label(
                                label="Demand",
                                html_for="crossfilter-demand",
                                icon_class="bi bi-graph-up",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "decorative": True,
                                },
                            ),
                            dropdown(
                                options=MOBILITY_DEMAND,
                                id="crossfilter-demand",
                            ),
                        ],
                        id="demand-col",
                    )
                ),
            ],
        ),
        id="scenario-params-row",
        style=basic_style,
    )


def scenario_parameters():
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Scenario parameters"),
                icon_class="bi bi-map",
                icon_style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
                button_label="What do these do?",
                button_id="scenario-info-button",
            ),
            collapse(
                id="scenario-info-collapse",
                text="""
                These buttons build your very own simulated city ("scenario" for short)!

                * *Season* controls the weather conditions - keeping the winters cool and summers hot! Bikers love it.
                * *Time of week* refers to what day should be simulated. *Weekday* means it is time to hurry to work between Monday and Friday and *Weekend* is for that relaxed sightseeing on Saturday or Sunday.
                * *Area* changes what area is being simulated. Trying to take it all in all at once made our head spin (the AI's too), so we made a tour around the city instead.
                * *Demand* decides how much mobility is going on. *Regular* projection refers to what one would expect to see based on the historical data; *Low* scales the regular projection down by 20%, while *High* increases it by 20%.
                """,
            ),
            _scenario_parameter_row(),
        ],
        id="scenario-div",
        style=basic_style,
    )


def optimization_parameters():
    """Renders the optimization parameters section."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Optimization parameters"),
                icon_class="bi bi-gear",
                icon_style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
                button_id="optimization-info-button",
                button_label="Now you lost me!",
            ),
            collapse(
                id="optimization-info-collapse",
                text="""
                Tuning *Priority* to your liking before pressing **Simulate** makes the AI do your personal bidding in the city renovation! Priority signals to AI how important the objective is for you. When the AI runs into a tie, the most important objective wins the round and the optimization game continues. Note that air quality and livability go hand in hand, as air quality is the only variable we play with for livability formulas.
                """,
            ),
            html.P(
                "Priority",
                style={
                    "fontSize": "1.35em",
                    "paddingTop": "1vh",
                    "paddingBottom": "1vh",
                },
            ),
            html.Div(
                optimization_row(
                    objective=OBJECTIVES[1],
                    icon_class="bi bi-car-front-fill",
                ),
            ),
            html.Div(
                optimization_row(
                    objective=OBJECTIVES[2],
                    icon_class="bi bi-wind",
                ),
            ),
            html.Div(
                optimization_row(
                    objective=OBJECTIVES[3],
                    icon_class="bi bi-house-heart-fill",
                ),
            ),
        ],
        id="optimization-div",
        style=basic_style,
    )


def simulation_button():
    """Renders the simulate button."""
    return html.Div(
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
                ),
                style={
                    "paddingTop": "3vh",
                    "paddingBottom": "3vh",
                    "display": "block",
                },
            ),
            html.Hr(),
        ],
        style=basic_style,
    )


def _objective_tabs():
    return html.Div(
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
        id="results-tabs-div",
        style=basic_style,
    )


def results_tabs():
    """Renders the results tabs."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Results"),
                icon_class="bi bi-bar-chart-line",
                icon_style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
                button_id="results-info-button",
                button_label="Explain, please!",
            ),
            collapse(
                id="results-info-collapse",
                text="""
                There is a lot going on in the city - a bit too much, which is why we brought you tabs. *Summary* lets you see the big picture "before" (*Baseline*) and "after" (*Optimized*) the AI renovation, while the other tabs – *Traffic*, *Air quality* and *Livability* – zoom in one objective and different variables related to that objective.
                """,
            ),
            _objective_tabs(),
        ],
        style=basic_style,
    )


def app_layout():
    """Main function to serve the complete application layout."""
    return html.Div(
        [
            project_info(),
            scenario_parameters(),
            optimization_parameters(),
            simulation_button(),
            results_tabs(),
            viz_params(),
            plot_results(),
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
