from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from utils.constants import (
    SEASONS,
    WEEKDAYS,
    MOBILITY_DEMAND,
    AREAS,
    TIMELINE_OPTIONS,
    OBJECTIVES,
    OPTIM_MARKS,
    SITUATIONS,
)

basic_style = {"paddingTop": "2vh", "paddingBottom": "2vh"}
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]


def performance_threshold(objective):
    return html.Center(
        html.Div(
            [
                daq.NumericInput(
                    value=100,
                    id=f"{objective.lower()}-optim-threshold",
                    min=0,
                    max=100,
                    label="% of improvement",
                    labelPosition="bottom",
                    style={
                        "display": "inline-block",
                        "fontSize": 18,
                        "paddingRight": "1vw",
                    },
                ),
            ]
        )
    )


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
                align="center",
                width={"size": 3},
            ),
            dbc.Col(
                html.Div(
                    dcc.Slider(
                        step=None,
                        marks={
                            i: {
                                "label": f"{OPTIM_MARKS[i]}",
                                "style": {"fontSize": "1.2em"},
                            }
                            for i in range(len(OPTIM_MARKS))
                        },
                        value=0,
                        id=f"{objective.lower()}-priority",
                    ),
                ),
                # Vertical align
                align="center",
            ),
            # dbc.Col(performance_threshold(objective)),
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
            style={"paddingTop": "2vh", "paddingBottom": "4vh", "width": "auto"},
        ),
        style=basic_style,
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
    header, button_label, button_id, icon_class=None, icon_style=None
):
    return html.Div(
        [
            # Page title
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
                        # width=True,
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
    )


def dropdown(options, value, id, style={"font-size": 18, "width": True}):
    return html.Div(
        dcc.Dropdown(
            options=options,
            value=value,
            id=id,
            style=style,
        )
    )


def labeled_parameter(label, parameter, html_for, icon_class=None, icon_style=None):
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
            parameter,
        ],
        style=basic_style,
    )


def twin_radio_buttons(options, value, id):
    return html.Div(
        dcc.RadioItems(
            options=options,
            value=value,
            id=id,
            inline=True,
            labelStyle={
                "automargin": True,
                "paddingTop": "1vh",
                "fontSize": 18,
                "paddingRight": "1vw",
            },
            inputStyle={"margin-right": "0.3vw"},
        ),
        style=basic_style,
    )


def graph_with_location_text_and_button(plot_id, text_id, button_id):
    return html.Div(
        [
            # Centering
            html.Center(
                html.Div(
                    [
                        # The graph
                        dcc.Loading(
                            dcc.Graph(
                                id=plot_id,
                                responsive=True,
                                config={"showTips": True},
                                style={"height": "45vw", "width": "68vw"},
                            ),
                            type="cube",
                        ),
                        # Location text
                        html.P(
                            id=text_id,
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
                            id=button_id,
                            n_clicks=0,
                            style={
                                "display": "block",
                                "font-size": "0.75em",
                                "automargin": True,
                                "padding": "1vh",
                            },
                        ),
                    ]
                ),
            ),
        ]
    )


def tab_layout(objective, variables):
    first = None
    if objective == OBJECTIVES[0]:
        # Summary of AI actions
        first = html.Div(
            dcc.Loading(
                dcc.Markdown(
                    id=f"{objective.lower()}-one",
                    style={"height": "30vw"},
                ),
                type="cube",
                style={"display": "none"},
            ),
            id=f"{objective.lower()}-one-div",
            style=basic_style,
        )
    elif objective == OBJECTIVES[3]:
        # Livability graphs
        first = html.Div(
            [
                # Situation buttons
                labeled_parameter(
                    label="Situation",
                    parameter=twin_radio_buttons(
                        options=SITUATIONS,
                        value=SITUATIONS[0],
                        id=f"crossfilter-{objective.lower()}-situation",
                    ),
                    html_for=f"crossfilter-{objective.lower()}-situation",
                    icon_class="bi bi-check-circle",
                    icon_style={
                        "paddingRight": "20px",
                        "fontSize": "1.75em",
                        "decorative": True,
                    },
                ),
                html.H2(
                    f"{objective.capitalize()} work in progress!",
                    id=f"{objective.lower()}-one",
                ),
            ],
            id=f"{objective.lower()}-one-div",
            style=basic_style,
        )
    else:
        first = html.Div(
            [
                # Situation buttons
                labeled_parameter(
                    label="Situation",
                    parameter=twin_radio_buttons(
                        options=SITUATIONS,
                        value=SITUATIONS[0],
                        id=f"crossfilter-{objective.lower()}-situation",
                    ),
                    html_for=f"crossfilter-{objective.lower()}-situation",
                    icon_class="bi bi-check-circle",
                    icon_style={
                        "paddingRight": "20px",
                        "fontSize": "1.75em",
                        "decorative": True,
                    },
                ),
                # Variable dropdown
                labeled_parameter(
                    label="Variable",
                    html_for=f"crossfilter-{objective.lower()}-variable",
                    parameter=dropdown(
                        options=variables,
                        value=variables[0],
                        id=f"crossfilter-{objective.lower()}-variable",
                        style={"font-size": 18, "width": "25vw"},
                    ),
                    icon_class="bi bi-search",
                    icon_style={
                        "paddingRight": "20px",
                        "fontSize": "1.75em",
                        "decorative": True,
                    },
                ),
                # First div
                html.Div(
                    graph_with_location_text_and_button(
                        plot_id=f"{objective.lower()}-one",
                        text_id=f"{objective.lower()}-location-text",
                        button_id=f"{objective.lower()}-location",
                    ),
                    style={"display": "none"},
                ),
            ],
            id=f"{objective.lower()}-one-div",
            style=basic_style,
        )
    return html.Center(
        html.Div(
            [
                # First div
                first,
                # Second div
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id=f"{objective.lower()}-two",
                            responsive=True,
                            style={"height": "30vw"},
                        ),
                        type="cube",
                    ),
                    id=f"{objective.lower()}-two-div",
                    style={"display": "none"},
                ),
                # Third div
                html.Div(
                    dcc.Loading(
                        dcc.Graph(
                            id=f"{objective.lower()}-three",
                            responsive=True,
                            style={"height": "30vw"},
                        ),
                        type="cube",
                    ),
                    id=f"{objective.lower()}-three-div",
                    style={"display": "none"},
                ),
            ],
            id=f"{objective.lower()}-tab-div",
            style=basic_style,
        )
    )


def project_info_section():
    """Renders the project info section."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H1(
                    "AI-based optimisation tool for sustainable urban planning (AIOSut)",
                    style={"width": "80vw"},
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
            html.Hr(),  # Dividing line
        ],
        style=basic_style,
    )


def scenario_parameters_section():
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Scenario parameters", style={"width": "80vw"}),
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
                * *Demand* decides how much mobility is going on. *Regular* projection refers to what one would expect to see based on the historical data; *Low* scales the regular projection down by 20%, while *High* increases it by 20%.
                * *Area* changes what area is being simulated. Trying to take it all in all at once made our head spin (the AI's too), so we made a tour around the city instead.
                """,
            ),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            labeled_parameter(
                                label="Season",
                                html_for="crossfilter-season",
                                parameter=dropdown(
                                    options=SEASONS,
                                    value=SEASONS[0],
                                    id="crossfilter-season",
                                ),
                                icon_class="bi bi-cloud-sun",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            )
                        ),
                        dbc.Col(
                            labeled_parameter(
                                label="Time of week",
                                html_for="crossfilter-time",
                                parameter=dropdown(
                                    options=WEEKDAYS,
                                    value=WEEKDAYS[0],
                                    id="crossfilter-time",
                                ),
                                icon_class="bi bi-calendar-day",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            )
                        ),
                        dbc.Col(
                            labeled_parameter(
                                label="Area",
                                html_for="crossfilter-area",
                                parameter=dropdown(
                                    options=AREAS,
                                    value=AREAS[1],
                                    id="crossfilter-area",
                                ),
                                icon_class="bi bi-geo-alt",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            )
                        ),
                        dbc.Col(
                            labeled_parameter(
                                label="Demand",
                                html_for="crossfilter-demand",
                                parameter=dropdown(
                                    options=MOBILITY_DEMAND,
                                    value=MOBILITY_DEMAND[1],
                                    id="crossfilter-demand",
                                ),
                                icon_class="bi bi-graph-up",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            )
                        ),
                    ],
                    align="top",
                ),
                style=basic_style,
            ),
            html.Hr(),  # Dividing line
        ],
        style=basic_style,
    )


def optimization_parameters_section():
    """Renders the optimization parameters section."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Optimization parameters", style={"width": "80vw"}),
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
                # text="""
                # Tuning these parameters to your liking before pressing *Simulate* makes the AI do your bidding in the city renovation!
                # * *Priority* refers to how important the objective is for you. When the AI runs into a tie, the most important objective wins one round of rock-paper-scissors and the game continues.
                # * *Performance thresholds* - because sometimes, one doesn't need to go all the way and instead just do good enough! By decreasing the threshold, you are telling AI "it is okay to rest when you reach _this much_ improvement for a given objective, with respect to the baseline". As a bonus, the results are returned quicker! When set at *100*, the AI returns its ultimate best effort at the solution.
                # """,
                text="""
                Tuning *Priority* to your liking before pressing **Simulate** makes the AI do your personal bidding in the city renovation! Priority signals to AI how important the objective is for you. When the AI runs into a tie, the most important objective wins the round and the optimization game continues. Note that air quality and livability go hand in hand, as air quality is the only variable we play with for livability formulas.
                """,
            ),
            optimization_row(
                objective=OBJECTIVES[1],
                icon_class="bi bi-car-front-fill",
            ),
            optimization_row(
                objective=OBJECTIVES[2],
                icon_class="bi bi-wind",
            ),
            optimization_row(
                objective=OBJECTIVES[3],
                icon_class="bi bi-house-heart-fill",
            ),
        ],
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


def visualization_parameters_section():
    """Renders the visualization parameters section."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Visualization parameters", style={"width": "80vw"}),
                icon_class="bi bi-filter",
                icon_style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
                button_id="visualization-info-button",
                button_label="Hold on a minute!",
            ),
            collapse(
                id="visualization-info-collapse",
                text="""
                When you get your BIG dataset back, not every second needs to be recorded there as is, right?
                * *Timestep interval* adjusts how many seconds are squeezed into one data point. By default, every 60 seconds are squeezed into "1" minute, resulting in 60 data points out of one hour with 3 600 seconds. For example, "15" minutes would squeeze every 900 seconds into one data point, making up for four (3 600 / 900) data points. Naturally, you are free to squeeze as long as there is time juice left in the simulation!
                * *Temporal aggregation* defines the method how the seconds are squeezed inside a given time range. "Sum" just sums everything&#42 together, while "Average" takes the mean of everything&#42. For example: "Sum": `[1,2,3] -> 6`; "Average": `[1,2,3] -> 2`.
                
                &#42Well, everything except for average values, Speed and Noise as we can't provide speed of light -travelling or hearing aids here, sorry! Instead, Speed gets averaged always, Noise has its own formula called Harmonoise and averages will always be averages.
                """,
            ),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            labeled_parameter(
                                label="Timestep interval",
                                html_for="crossfilter-timestep-range",
                                parameter=html.Div(
                                    [
                                        daq.NumericInput(
                                            value=1,
                                            id="crossfilter-timestep-range",
                                            min=1,
                                            max=60,
                                            size=70,
                                            style={
                                                # "fontSize": "1.3em",
                                                "float": "left",
                                            },
                                            label={
                                                "label": "minute(s)",
                                                "style": {
                                                    "fontSize": "0.9em",
                                                },
                                            },
                                            labelPosition="bottom",
                                        ),
                                    ],
                                    style={"paddingTop": "2vh", "fontSize": "1.3em"},
                                ),
                                icon_class="bi bi-clock",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            labeled_parameter(
                                label="Temporal aggregation",
                                html_for="crossfilter-timeline-type",
                                parameter=twin_radio_buttons(
                                    options=TIMELINE_OPTIONS,
                                    value=TIMELINE_OPTIONS[0],
                                    id="crossfilter-timeline-type",
                                ),
                                icon_class="bi bi-stack",
                                icon_style={
                                    "paddingRight": "20px",
                                    "fontSize": "1.75em",
                                    "float": "left",
                                    "decorative": True,
                                },
                            ),
                            width=4,
                        ),
                    ],
                    align="center",
                    justify="start",
                ),
                # style=basic_style,
            ),
            html.Hr(),  # Dividing line
        ],
        style=basic_style,
    )


def results_section():
    """Renders the results section with tabs."""
    return html.Div(
        [
            header_and_info_button_row(
                header=html.H2("Results", style={"width": "80vw"}),
                icon_class="bi bi-bar-chart-line",
                icon_style={
                    "paddingRight": "20px",
                    "fontSize": "1.75em",
                    "float": "left",
                    "decorative": True,
                },
                button_id="results-info-button",
                button_label="Tell me more, please!",
            ),
            collapse(
                id="results-info-collapse",
                text="""
                There is a lot going on in the city - a bit too much, which is why we brought you tabs. *Summary* lets you see the big picture "before" (*Baseline*) and "after" (*Optimized*) the AI renovation, re-counting AI's side of the story, while the other tabs – *Traffic*, *Air quality* and *Livability* – zoom in one objective and different variables related to that objective.
                
                FYI: *Baseline* corresponds to the city as of now, using various data recorded all over the city in 2018 that is projected to 2025. That's how our simulation gets real!
                """,
            ),
            dcc.Tabs(
                id="results-tabs",
                # value="traffic",
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
            html.Div(
                id="results-tabs-content-1",
            ),
        ],
        style=basic_style,
    )


def app_layout():
    """Main function to serve the complete application layout."""
    return html.Div(
        [
            project_info_section(),
            scenario_parameters_section(),
            optimization_parameters_section(),
            simulation_button(),
            visualization_parameters_section(),
            results_section(),
        ],
        style={"width": "99vw", "automargin": True, "padding": "5vh 5vh 5vh 5vh"},
    )
