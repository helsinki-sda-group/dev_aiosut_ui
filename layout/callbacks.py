from dash import Input, Output, State, dcc, html
import utils.helpers as uh
import utils.constants as uc
import layout.components as lc
import pandas as pd
import numpy as np

basic_style = {"paddingTop": "2vh", "paddingBottom": "2vh"}
empty_style = {"display": "none"}


def register_callbacks(app):
    @app.callback(
        Output("project-info-collapse", "is_open"),
        Input("project-info-button", "n_clicks"),
        State("project-info-collapse", "is_open"),
    )
    def toggle_project_info_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("scenario-info-collapse", "is_open"),
        Input("scenario-info-button", "n_clicks"),
        State("scenario-info-collapse", "is_open"),
    )
    def toggle_scenario_info_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # @app.callback(
    #     Output("optimization-info-collapse", "is_open"),
    #     Input("optimization-info-button", "n_clicks"),
    #     State("optimization-info-collapse", "is_open"),
    # )
    # def toggle_optimization_info_collapse(n, is_open):
    #     if n:
    #         return not is_open
    #     return is_open

    @app.callback(
        Output("filter-info-collapse", "is_open"),
        Input("filter-info-button", "n_clicks"),
        State("filter-info-collapse", "is_open"),
    )
    def toggle_filter_info_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("results-info-collapse", "is_open"),
        Input("results-info-button", "n_clicks"),
        State("results-info-collapse", "is_open"),
    )
    def toggle_results_info_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # # TODO: Check if simulation data is available, and if not, ask permission to proceed to simulate
    # @app.callback(
    #     [
    #         Input("simulate-button", "n_clicks"),
    #         Input("crossfilter-season", "value"),
    #         Input("crossfilter-time", "value"),
    #         Input("crossfilter-area", "value"),
    #         Input("crossfilter-demand", "value"),
    #         Input("traffic-priority", "value"),
    #     ],
    #     # State("progress-bar", "label"),
    # )
    # def simulate_data(button_clicks, season, time, area, demand, traffic_priority):
    #     if button_clicks > 0:
    #         print("Simulation in progress!")
    #         return
    #     else:
    #         pass

    @app.callback(
        [
            Output("viz-div", "style"),
            Output("situation-div", "style"),
            Output("variable-div", "style"),
            Output("crossfilter-variable", "options"),
            # Output("timestep-div", "style"),
            # Output("timeline-div", "style"),
            Output("visualize-button", "style"),
        ],
        Input("results-tabs", "value"),
    )
    def show_viz_parameters(tab):
        if tab == lc.OBJECTIVES[1]:
            return [
                basic_style,
                basic_style,
                basic_style,
                uc.TRAFFIC_VARIABLES,
                # basic_style,
                # basic_style,
                {"fontSize": "1.2em"},
            ]
        elif tab == lc.OBJECTIVES[2]:
            return [
                basic_style,
                basic_style,
                basic_style,
                uc.AQ_VARIABLES,
                # basic_style,
                # basic_style,
                {"fontSize": "1.2em"},
            ]
        elif tab == lc.OBJECTIVES[3]:
            return [
                basic_style,
                basic_style,
                empty_style,
                empty_style,
                # empty_style,
                # empty_style,
                {"fontSize": "1.2em"},
            ]
        else:
            return [
                empty_style,
                empty_style,
                empty_style,
                empty_style,
                # empty_style,
                # empty_style,
                empty_style,
            ]

    @app.callback(
        [
            Output("timestep-div", "style"),
            Output("timeline-div", "style"),
        ],
        [
            State("results-tabs", "value"),
            Input("crossfilter-variable", "value"),
        ],
    )
    def hide_params(tab, variable):
        if tab in [uc.OBJECTIVES[0], uc.OBJECTIVES[3]]:
            return empty_style, empty_style
        elif tab == uc.OBJECTIVES[1] and variable in ["Travel time", "Lost time"]:
            return empty_style, empty_style
        else:
            return basic_style, basic_style

    @app.callback(
        [
            Output("figure-one-div", "children"),
            Output("figure-two-div", "children"),
            Output("figure-three-div", "children"),
            Output("figure-four-div", "children"),
            Output("summary-text", "children"),
            # Output("location-text", "children"),
        ],
        [
            # Input("figure-one", "clickData"),
            Input("visualize-button", "n_clicks"),
            Input("results-tabs", "value"),
            State("crossfilter-season", "value"),
            State("crossfilter-time", "value"),
            State("crossfilter-area", "value"),
            State("crossfilter-demand", "value"),
            State("traffic-priority", "value"),
            State("crossfilter-situation", "value"),
            State("crossfilter-variable", "value"),
            State("crossfilter-timeline-type", "value"),
            State("crossfilter-timestep", "value"),
        ],
    )
    def show_graphs(
        # spatial_click_data,
        n_clicks,
        tab,
        season,
        time,
        area,
        demand,
        traffic_priority,
        situation,
        variable,
        timeline_type,
        timestep_range,
    ):
        params = [
            season,
            time,
            area,
            demand,
            traffic_priority,
            situation,
            variable,
            timeline_type,
            timestep_range,
        ]
        all_params_ready = all(param is not None for param in params)
        # Initialize outputs
        first_plot = []
        second_plot = []
        third_plot = []
        fourth_plot = []
        summary_text = []
        # current_location = """Location: Network"""
        # Summary
        if tab == lc.OBJECTIVES[0]:
            summary_text = dcc.Markdown(
                """Summary WIP!""",
                style={
                    "paddingTop": "2vh",
                    "paddingBottom": "2vh",
                    "fontSize": "1.2em",
                },
            )

            # Traffic KPI and mobility mode
            baseline_traffic_network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation="Baseline",
                variable="Travel time",
            )
            baseline_avg_travel_network = (
                baseline_traffic_network.groupby(["Mobility mode"], observed=False)
                .agg({"Travel time": "mean", "Mobility flow": "sum"})
                .reset_index()
            )

            optimized_traffic_network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation="Optimized",
                variable="Travel time",
            )

            optimized_avg_travel_network = (
                optimized_traffic_network.groupby(["Mobility mode"], observed=False)
                .agg({"Travel time": "mean", "Mobility flow": "sum"})
                .reset_index()
            )

            mobility_flow_bar = uh.create_traffic_situation_bar_plot(
                optimized_network=optimized_avg_travel_network,
                baseline_network=baseline_avg_travel_network,
                variable="Mobility flow",
                xaxis_title=f"Mobility flow\n({uc.UNITS['Mobility flow']})",
            )
            first_plot = dcc.Graph(
                figure=mobility_flow_bar,
                responsive=True,
                style={
                    "height": "30vw",
                    "paddingBottom": "2vh",
                    "paddingTop": "2vh",
                },
            )

            travel_time_bar = uh.create_traffic_situation_bar_plot(
                optimized_network=optimized_avg_travel_network,
                baseline_network=baseline_avg_travel_network,
                variable="Travel time",
                xaxis_title=f"Average travel time\n({uc.UNITS['Travel time']})",
            )
            second_plot = dcc.Graph(
                figure=travel_time_bar,
                responsive=True,
                style={
                    "height": "30vw",
                    "paddingBottom": "2vh",
                    "paddingTop": "2vh",
                },
            )

            # AQ KPI
            baseline_AQ_network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation="Baseline",
                variable="Respirable particles",
            )
            baseline_avg_AQ_network = pd.DataFrame(
                data={
                    "Respirable particles": [
                        baseline_AQ_network["Respirable particles"].mean()
                    ]
                }
            )

            optimized_AQ_network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation="Optimized",
                variable="Respirable particles",
            )
            optimized_avg_AQ_network = pd.DataFrame(
                data={
                    "Respirable particles": [
                        optimized_AQ_network["Respirable particles"].mean()
                    ]
                }
            )

            aq_bar = uh.create_situation_bar_plot(
                optimized_network=optimized_avg_AQ_network,
                baseline_network=baseline_avg_AQ_network,
                variable="Respirable particles",
                xaxis_title=f"Average respirable particles\n({uc.UNITS['Respirable particles']})",
            )
            third_plot = dcc.Graph(
                figure=aq_bar,
                responsive=True,
                style={
                    "height": "30vw",
                    "paddingBottom": "2vh",
                    "paddingTop": "2vh",
                },
            )

            # Livability KPI
            # baseline_livability_network = uh.get_data(
            #     area=area,
            #     season=season,
            #     time=time,
            #     demand=demand,
            #     optimization=traffic_priority,
            #     situation=situation,
            #     variable="Relocation rate",
            # )
            # optimized_livability_network = uh.get_data(
            #     area=area,
            #     season=season,
            #     time=time,
            #     demand=demand,
            #     optimization=traffic_priority,
            #     situation=situation,
            #     variable="Relocation rate",
            # )
        # Livability
        elif tab == lc.OBJECTIVES[3] and situation is not None:
            summary_text = dcc.Markdown(
                """Livability WIP!""",
                style={
                    "paddingTop": "2vh",
                    "paddingBottom": "2vh",
                    "fontSize": "1.2em",
                },
            )
        elif tab == lc.OBJECTIVES[1] and variable in ["Travel time", "Lost time"]:
            network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation=situation,
                variable=variable,
            )
            # Draw the histogram
            histogram = uh.create_mobility_mode_histogram(
                network=network, variable=variable
            )
            second_plot = dcc.Graph(
                figure=histogram,
                responsive=True,
                style={"height": "30vw"},
            )

            # Calculate data
            barplot_network = (
                network.groupby(["Mobility mode"])
                .agg({variable: "mean", "Mobility flow": "sum"})
                .reset_index()
            )
            # Draw the bar plot
            bar_plot = uh.create_mobility_mode_avg_bar_plot(
                network=barplot_network, variable=variable
            )
            bar_plot.update_layout(xaxis_title=f"Average {variable.lower()} in seconds")
            # Output the plot
            third_plot = dcc.Graph(
                figure=bar_plot,
                responsive=True,
                style={
                    "height": "30vw",
                    "paddingBottom": "2vh",
                    "paddingTop": "2vh",
                },
            )
        # Params required
        elif all_params_ready:
            # Mobility flow
            if tab == lc.OBJECTIVES[1] and variable == "Mobility flow":
                # Calculate data
                network = uh.get_data(
                    area=area,
                    season=season,
                    time=time,
                    demand=demand,
                    optimization=traffic_priority,
                    situation=situation,
                    variable=variable,
                )
                network = uh.new_timeline(
                    network=network, timestep_range=timestep_range
                )
                # network, current_location = uh.spatial_scope(
                #     spatial_click_data, network
                # )
                heatmap_network = (
                    network.groupby(["Timestep", "Edge"], observed=False)
                    .agg(
                        {
                            variable: "sum",
                            "Longitude": "first",
                            "Latitude": "first",
                            "Name": "first",
                        }
                    )
                    .reset_index()
                )
                if timeline_type == "mean":
                    heatmap_network[variable] = (
                        heatmap_network[variable] / timestep_range
                    )
                # Draw the heatmap
                heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
                first_plot = dcc.Graph(
                    figure=heatmap,
                    responsive=True,
                    style={
                        "height": "50vw",
                        "width": "55vw",
                        "paddingBottom": "2vh",
                    },
                )

                # Calculate data
                if timeline_type == "mean":
                    area_network = (
                        network.groupby(
                            ["Mobility mode", "Simulation timestep", "Timestep"],
                            observed=False,
                        )
                        .agg({"Vehicle": lambda x: x.nunique()})
                        .reset_index()
                    )
                    area_network = (
                        area_network.groupby(
                            ["Mobility mode", "Timestep"], observed=False
                        )
                        .agg({"Vehicle": timeline_type})
                        .reset_index()
                    )
                    area_network.fillna(value={"Vehicle": 0})

                elif timeline_type == "sum":
                    area_network = (
                        network.groupby(["Mobility mode", "Timestep"], observed=False)
                        .agg({"Vehicle": lambda x: x.nunique()})
                        .reset_index()
                    )
                    area_network = (
                        area_network.groupby(
                            ["Mobility mode", "Timestep"], observed=False
                        )
                        .agg({"Vehicle": timeline_type})
                        .reset_index()
                    )
                    area_network.fillna(value={"Vehicle": 0})

                # Draw the area chart
                area_plot = uh.create_area_chart(
                    network=area_network, variable="Vehicle"
                )
                third_plot = dcc.Graph(
                    figure=area_plot,
                    responsive=True,
                    style={
                        "height": "30vw",
                        "paddingBottom": "2vh",
                        "paddingTop": "2vh",
                    },
                )

            elif tab == lc.OBJECTIVES[1] and variable == "Noise":
                # Calculate the data
                network = uh.get_data(
                    area=area,
                    season=season,
                    time=time,
                    demand=demand,
                    optimization=traffic_priority,
                    situation=situation,
                    variable=variable,
                )
                network = uh.new_timeline(
                    network=network, timestep_range=timestep_range
                )
                second_network = uh.get_data(
                    area=area,
                    season=season,
                    time=time,
                    demand=demand,
                    optimization=traffic_priority,
                    situation=situation,
                    variable="Noise2",
                )
                second_network = uh.new_timeline(
                    network=second_network, timestep_range=timestep_range
                )
                # network, current_location = uh.spatial_scope(
                #     spatial_click_data, network
                # )
                # helper_network = (
                #     second_network.groupby(["Timestep", "Edge"], observed=False)
                #     .agg(
                #         {
                #             "Mobility flow": "sum",
                #         }
                #     )
                #     .reset_index()
                # )
                # network = network.merge(
                #     helper_network[["Edge", "Mobility flow", "Timestep"]],
                #     on=["Edge", "Timestep"],
                #     how="left",
                # )
                # print(network.head())
                heatmap_network = (
                    network.groupby(["Timestep", "Edge"], observed=False)
                    .agg(
                        {
                            variable: "mean",
                            "Longitude": "first",
                            "Latitude": "first",
                            "Name": "first",
                            "Mobility flow": "sum",
                        }
                    )
                    .reset_index()
                )
                heatmap_network.fillna(value={variable: 0})
                # Draw the heatmap
                heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
                first_plot = html.Div(
                    [
                        dcc.Graph(
                            figure=heatmap,
                            responsive=True,
                            style={
                                "height": "50vw",
                                "width": "55vw",
                                "paddingBottom": "2vh",
                            },
                        ),
                        lc.plots_location_text,
                        lc.plots_reset_button,
                    ]
                )

                # Calculate the data
                barplot_network = (
                    second_network.groupby(["Mobility mode"], observed=False)
                    .agg({variable: "mean", "Vehicle": pd.Series.nunique})
                    .reset_index()
                )
                # barplot_network["Vehicle average"] = np.round(
                #     barplot_network[variable] / barplot_network["Mobility flow"], 4
                # )
                # Draw the bar plot
                bar_plot = uh.create_mobility_mode_avg_bar_plot(
                    network=barplot_network, variable=variable
                )
                # Output the plot
                second_plot = dcc.Graph(
                    figure=bar_plot,
                    responsive=True,
                    style={"height": "30vw"},
                )

                # Calculate the data
                area_network = (
                    second_network.groupby(
                        ["Mobility mode", "Timestep"], observed=False
                    )
                    .agg({"Vehicle": pd.Series.nunique, variable: "mean"})
                    .reset_index()
                )

                # Draw the area chart
                area_plot = uh.create_area_chart(
                    network=area_network, variable=variable
                )
                # area_plot.update_layout(
                #     labels={"Vehicle": "Mobility flow"},
                # )
                third_plot = dcc.Graph(
                    figure=area_plot,
                    responsive=True,
                    style={
                        "height": "30vw",
                        "paddingBottom": "2vh",
                        "paddingTop": "2vh",
                    },
                )

            # Noise
            # Heatmap + bar plot + area chart
            elif tab == lc.OBJECTIVES[1] and variable == "Speed":
                # Calculate the data
                network = uh.get_data(
                    area=area,
                    season=season,
                    time=time,
                    demand=demand,
                    optimization=traffic_priority,
                    situation=situation,
                    variable=variable,
                )
                network = uh.new_timeline(
                    network=network, timestep_range=timestep_range
                )
                # network, current_location = uh.spatial_scope(
                #     spatial_click_data, network
                # )
                heatmap_network = (
                    network.groupby(["Timestep", "Edge"], observed=False)
                    .agg(
                        {
                            variable: "mean",
                            "Longitude": "first",
                            "Latitude": "first",
                            "Name": "first",
                            "Mobility flow": timeline_type,
                        }
                    )
                    .reset_index()
                )
                # Draw the heatmap
                heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
                first_plot = html.Div(
                    [
                        dcc.Graph(
                            figure=heatmap,
                            responsive=True,
                            style={
                                "height": "50vw",
                                "width": "55vw",
                                "paddingBottom": "2vh",
                            },
                        ),
                        lc.plots_location_text,
                        lc.plots_reset_button,
                    ]
                )

                # Calculate the data
                barplot_network = (
                    network.groupby(["Mobility mode"], observed=False)
                    .agg({variable: "mean", "Vehicle": lambda x: x.nunique()})
                    .reset_index()
                )
                # barplot_network["Vehicle average"] = np.round(
                #     barplot_network[variable] / barplot_network["Mobility flow"], 4
                # )
                # Draw the bar plot
                bar_plot = uh.create_mobility_mode_avg_bar_plot(
                    network=barplot_network, variable=variable
                )
                # Output the plot
                second_plot = dcc.Graph(
                    figure=bar_plot,
                    responsive=True,
                    style={"height": "30vw"},
                )

                # Calculate the data
                # area_network = (
                #     network.groupby(["Timestep"], observed=False)
                #     .agg(
                #         {
                #             variable: timeline_type,
                #             "Mobility flow": timeline_type,
                #             "Mobility mode": "first",
                #         }
                #     )
                #     .reset_index()
                # )
                # # Draw the area chart
                # area_plot = uh.create_area_chart(
                #     network=area_network, variable=variable
                # )
                # Calculate data
                # if timeline_type == "mean":
                #     # area_network = (
                #     #     network.groupby(
                #     #         ["Mobility mode", "Simulation timestep", "Timestep"],
                #     #         observed=False,
                #     #     )
                #     #     .agg({"Vehicle": pd.Series.nunique, variable: "median"})
                #     #     .reset_index()
                #     # )
                #     area_network = (
                #         network.groupby(
                #             ["Mobility mode", "Timestep"], observed=False
                #         )
                #         .agg({"Vehicle": pd.Series.nunique, variable: "mean"})
                #         .reset_index()
                #     )
                # elif timeline_type == "sum":
                area_network = (
                    network.groupby(["Mobility mode", "Timestep"], observed=False)
                    .agg({"Vehicle": lambda x: x.nunique(), variable: "mean"})
                    .reset_index()
                )

                # Draw the area chart
                area_plot = uh.create_area_chart(
                    network=area_network, variable=variable
                )
                # area_plot.update_layout(
                #     labels={"Vehicle": "Mobility flow"},
                # )
                third_plot = dcc.Graph(
                    figure=area_plot,
                    responsive=True,
                    style={
                        "height": "30vw",
                        "paddingBottom": "2vh",
                        "paddingTop": "2vh",
                    },
                )
            # AQ variables
            elif tab == lc.OBJECTIVES[2]:
                # Calculate the data
                network = uh.get_data(
                    area=area,
                    season=season,
                    time=time,
                    demand=demand,
                    optimization=traffic_priority,
                    situation=situation,
                    variable=variable,
                )
                network = uh.new_timeline(
                    network=network, timestep_range=timestep_range
                )
                # network, current_location = uh.spatial_scope(
                #     spatial_click_data, network
                # )
                heatmap_network = (
                    network.groupby(["Timestep", "Edge"], observed=False)
                    .agg(
                        {
                            variable: timeline_type,
                            "Longitude": "first",
                            "Latitude": "first",
                            "Name": "first",
                            "Mobility flow": timeline_type,
                        }
                    )
                    .reset_index()
                )
                # Draw the heatmap
                heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
                first_plot = html.Div(
                    [
                        dcc.Graph(
                            figure=heatmap,
                            responsive=True,
                            style={
                                "height": "50vw",
                                "width": "55vw",
                                "paddingBottom": "2vh",
                            },
                        ),
                        lc.plots_location_text,
                        lc.plots_reset_button,
                    ]
                )

                # Calculate the data
                barplot_network = (
                    network.groupby(["Mobility mode"], observed=False)
                    .agg({variable: "sum", "Mobility flow": "sum"})
                    .reset_index()
                )
                barplot_network["Vehicle average"] = np.round(
                    barplot_network[variable] / barplot_network["Mobility flow"], 4
                )
                # Draw the bar plot
                bar_plot = uh.create_mobility_mode_avg_bar_plot(
                    network=barplot_network, variable=variable
                )
                # Output the plot
                second_plot = dcc.Graph(
                    figure=bar_plot,
                    responsive=True,
                    style={"height": "30vw"},
                )

                # Calculate data
                if timeline_type == "mean":
                    area_network = (
                        network.groupby(
                            ["Mobility mode", "Simulation timestep", "Timestep"],
                            observed=False,
                        )
                        .agg(
                            {"Vehicle": lambda x: x.nunique(), variable: timeline_type}
                        )
                        .reset_index()
                    )
                    area_network = (
                        area_network.groupby(
                            ["Mobility mode", "Timestep"], observed=False
                        )
                        .agg({"Vehicle": timeline_type, variable: timeline_type})
                        .reset_index()
                    )
                elif timeline_type == "sum":
                    area_network = (
                        network.groupby(["Mobility mode", "Timestep"], observed=False)
                        .agg(
                            {"Vehicle": lambda x: x.nunique(), variable: timeline_type}
                        )
                        .reset_index()
                    )

                # Draw the area chart
                area_plot = uh.create_area_chart(network=area_network, variable="Vehicle")
                # Output the plot
                third_plot = dcc.Graph(
                    figure=area_plot,
                    responsive=True,
                    style={
                        "height": "30vw",
                        "paddingBottom": "2vh",
                        "paddingTop": "2vh",
                    },
                )

        # Return the figures, styles and location
        return [
            first_plot,
            second_plot,
            third_plot,
            fourth_plot,
            # current_location,
            summary_text,
        ]

    # @app.callback(
    #     Output("figure-one", "clickData"),
    #     [
    #         Input("reset-location", "n_clicks"),
    #     ],
    # )
    # def reset_location(reset):
    #     return None
