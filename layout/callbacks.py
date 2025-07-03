from dash import Input, Output, State
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

    @app.callback(
        Output("optimization-info-collapse", "is_open"),
        Input("optimization-info-button", "n_clicks"),
        State("optimization-info-collapse", "is_open"),
    )
    def toggle_optimization_info_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

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

    # # TODO
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
            Output("timestep-div", "style"),
            Output("timeline-div", "style"),
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
                basic_style,
                basic_style,
            ]
        elif tab == lc.OBJECTIVES[2]:
            return [
                basic_style,
                basic_style,
                basic_style,
                uc.AQ_VARIABLES,
                basic_style,
                basic_style,
            ]
        elif tab == lc.OBJECTIVES[3]:
            return [
                basic_style,
                basic_style,
                empty_style,
                empty_style,
                empty_style,
                empty_style,
            ]
        else:
            return [
                empty_style,
                empty_style,
                empty_style,
                empty_style,
                empty_style,
                empty_style,
            ]

    @app.callback(
        Output("summary-text", "children"),
        Output("summary-text-div", "style"),
        Output("figure-one", "figure"),
        Output("figure-two", "figure"),
        Output("figure-three", "figure"),
        Output("figure-four", "figure"),
        Output("location-text", "children"),
        Output("plots-div", "style"),
        [
            Input("results-tabs", "value"),
            Input("crossfilter-season", "value"),
            Input("crossfilter-time", "value"),
            Input("crossfilter-area", "value"),
            Input("crossfilter-demand", "value"),
            Input("traffic-priority", "value"),
            Input("crossfilter-situation", "value"),
            Input("crossfilter-variable", "value"),
            Input("crossfilter-timeline-type", "value"),
            Input("crossfilter-timestep", "value"),
            Input("figure-one", "clickData"),
        ],
    )
    def show_graphs(
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
        spatial_click_data,
    ):
        # Initialize output
        summary_text = ""
        summary_text_style = empty_style
        first_plot = {}
        second_plot = {}
        third_plot = {}
        fourth_plot = {}
        current_location = """"""
        plot_div_style = empty_style
        # Summary
        print(tab)
        if tab == lc.OBJECTIVES[0]:
            summary_text = """Summary WIP!"""
            summary_text_style = basic_style
            plot_div_style = basic_style
        # Livability
        elif tab == lc.OBJECTIVES[3]:
            summary_text = """Livability WIP!"""
            summary_text_style = basic_style
            plot_div_style = basic_style
        elif variable in ["Mobility flow"]:
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
            network = uh.new_timeline(network=network, timestep_range=timestep_range)
            network, current_location = uh.spatial_scope(spatial_click_data, network)
            heatmap_network = (
                network.groupby(["Timestep", "Edge"], observed=False)
                .agg(
                    {
                        variable: timeline_type,
                        "Longitude": "first",
                        "Latitude": "first",
                        "Name": "first",
                    }
                )
                .reset_index()
            )
            # Draw the heatmap
            heatmap = uh.create_heatmap(network=network, variable=variable)
            first_plot = heatmap

            # Calculate data
            if timeline_type == "Average":
                area_network = (
                    network.groupby(
                        ["Mobility mode", "Simulation timestep", "Timestep"],
                        observed=False,
                    )
                    .agg({"Vehicle": pd.Series.nunique})
                    .reset_index()
                )
                area_network = (
                    area_network.groupby(["Mobility mode", "Timestep"], observed=False)
                    .agg({"Vehicle": "mean"})
                    .reset_index()
                )
            elif timeline_type == "Sum":
                area_network = (
                    network.groupby(["Mobility mode", "Timestep"], observed=False)
                    .agg({"Vehicle": pd.Series.nunique})
                    .reset_index()
                )

            # Draw the area chart
            area_plot = uh.create_area_chart(network=network, variable=variable)
            third_plot = area_plot

        # Histogram + bar plot
        elif variable in ["Travel time", "Lost time"]:
            network = uh.get_data(
                area=area,
                season=season,
                time=time,
                demand=demand,
                optimization=traffic_priority,
                situation=situation,
                variable=variable,
            )
            # network = uh.new_timeline(network=network, timestep_range=timestep_range)
            # network, current_location = uh.spatial_scope(spatial_click_data, network)
            # Draw the histogram
            histogram = uh.create_mobility_mode_histogram(
                network=network, variable=variable
            )
            second_plot = histogram

            # Calculate data
            barplot_network = (
                network.groupby(["Mobility mode"])
                .agg({variable: "mean", "Mobility flow": "sum"})
                .reset_index()
            )
            # Draw the bar plot
            bar_plot = uh.create_mobility_mode_avg_bar_plot(
                network=network, variable=variable
            )
            # Output the plot
            third_plot = bar_plot

        # Heatmap + bar plot
        elif variable in ["Noise", "Speed"]:
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
            network = uh.new_timeline(network=network, timestep_range=timestep_range)
            network, current_location = uh.spatial_scope(spatial_click_data, network)
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
            first_plot = heatmap

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
            second_plot = bar_plot

            # Calculate the data
            area_network = (
                network.groupby(["Timestep"], observed=False)
                .agg(
                    {
                        variable: timeline_type,
                        "Mobility flow": timeline_type,
                        "Mobility mode": "first",
                    }
                )
                .reset_index()
            )
            # Draw the area chart
            area_plot = uh.create_area_chart(network=area_network, variable=variable)
            third_plot = area_plot

        # Return the figures, styles and location
        return (
            summary_text,
            summary_text_style,
            first_plot,
            second_plot,
            third_plot,
            fourth_plot,
            current_location,
            plot_div_style,
        )

    @app.callback(
        Output("figure-one", "clickData"),
        [
            Input("reset-location", "n_clicks"),
        ],
    )
    def reset_location(reset):
        return None


# @app.callback(
#     Output("traffic-one", "figure"),
#     Output("traffic-two", "figure"),
#     Output("traffic-three", "figure"),
#     Output("traffic-location-text", "children"),
#     [
#         Input("crossfilter-season", "value"),
#         Input("crossfilter-time", "value"),
#         Input("crossfilter-area", "value"),
#         Input("crossfilter-demand", "value"),
#         Input("traffic-priority", "value"),
#         Input("crossfilter-traffic-situation", "value"),
#         Input("crossfilter-traffic-variable", "value"),
#         Input("crossfilter-timeline-type", "value"),
#         Input("crossfilter-timestep-range", "value"),
#         Input("traffic-one", "clickData"),
#     ],
# )
# def update_traffic_graphs(
#     season,
#     time,
#     area,
#     demand,
#     traffic_priority,
#     situation,
#     variable,
#     timeline_type,
#     timestep_range,
#     spatial_click_data,
# ):
#     # Initialize output
#     first_plot = {}
#     second_plot = {}
#     third_plot = {}
#     current_location = ""

#     if variable in ["Mobility flow"]:
#         # Calculate data
#         network = uh.get_data(
#             area=area,
#             season=season,
#             time=time,
#             demand=demand,
#             optimization=traffic_priority,
#             situation=situation,
#             variable=variable,
#         )
#         network = uh.new_timeline(network=network, timestep_range=timestep_range)
#         network, current_location = uh.spatial_scope(spatial_click_data, network)
#         heatmap_network = (
#             network.groupby(["Timestep", "Edge"], observed=False)
#             .agg(
#                 {
#                     variable: timeline_type,
#                     "Longitude": "first",
#                     "Latitude": "first",
#                     "Name": "first",
#                 }
#             )
#             .reset_index()
#         )
#         # Draw the heatmap
#         heatmap = uh.create_heatmap(network=network, variable=variable)
#         first_plot = heatmap

#         # Calculate data
#         if timeline_type == "Average":
#             area_network = (
#                 network.groupby(
#                     ["Mobility mode", "Simulation timestep", "Timestep"],
#                     observed=False,
#                 )
#                 .agg({"Vehicle": pd.Series.nunique})
#                 .reset_index()
#             )
#             area_network = (
#                 area_network.groupby(["Mobility mode", "Timestep"], observed=False)
#                 .agg({"Vehicle": "mean"})
#                 .reset_index()
#             )
#         elif timeline_type == "Sum":
#             area_network = (
#                 network.groupby(["Mobility mode", "Timestep"], observed=False)
#                 .agg({"Vehicle": pd.Series.nunique})
#                 .reset_index()
#             )

#         # Draw the area chart
#         area_plot = uh.create_area_chart(network=network, variable=variable)
#         third_plot = area_plot

#     # Histogram + bar plot
#     elif variable in ["Travel time", "Lost time"]:
#         network = uh.get_data(
#             area=area,
#             season=season,
#             time=time,
#             demand=demand,
#             optimization=traffic_priority,
#             situation=situation,
#             variable=variable,
#         )
#         # network = uh.new_timeline(network=network, timestep_range=timestep_range)
#         # network, current_location = uh.spatial_scope(spatial_click_data, network)
#         # Draw the histogram
#         histogram = uh.create_mobility_mode_histogram(
#             network=network, variable=variable
#         )
#         second_plot = histogram

#         # Calculate data
#         barplot_network = (
#             network.groupby(["Mobility mode"])
#             .agg({variable: "mean", "Mobility flow": "sum"})
#             .reset_index()
#         )
#         # Draw the bar plot
#         bar_plot = uh.create_mobility_mode_avg_bar_plot(
#             network=network, variable=variable
#         )
#         # Output the plot
#         third_plot = bar_plot

#     # Heatmap + bar plot
#     elif variable in ["Noise", "Speed"]:
#         # Calculate the data
#         network = uh.get_data(
#             area=area,
#             season=season,
#             time=time,
#             demand=demand,
#             optimization=traffic_priority,
#             situation=situation,
#             variable=variable,
#         )
#         network = uh.new_timeline(network=network, timestep_range=timestep_range)
#         network, current_location = uh.spatial_scope(spatial_click_data, network)
#         heatmap_network = (
#             network.groupby(["Timestep", "Edge"], observed=False)
#             .agg(
#                 {
#                     variable: timeline_type,
#                     "Longitude": "first",
#                     "Latitude": "first",
#                     "Name": "first",
#                     "Mobility flow": timeline_type,
#                 }
#             )
#             .reset_index()
#         )
#         # Draw the heatmap
#         heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
#         first_plot = heatmap

#         # Calculate the data
#         barplot_network = (
#             network.groupby(["Mobility mode"], observed=False)
#             .agg({variable: "sum", "Mobility flow": "sum"})
#             .reset_index()
#         )
#         barplot_network["Vehicle average"] = np.round(
#             barplot_network[variable] / barplot_network["Mobility flow"], 4
#         )
#         # Draw the bar plot
#         bar_plot = uh.create_mobility_mode_avg_bar_plot(
#             network=barplot_network, variable=variable
#         )
#         # Output the plot
#         second_plot = bar_plot

#         # Calculate the data
#         area_network = (
#             network.groupby(["Timestep"], observed=False)
#             .agg(
#                 {
#                     variable: timeline_type,
#                     "Mobility flow": timeline_type,
#                     "Mobility mode": "first",
#                 }
#             )
#             .reset_index()
#         )
#         # Draw the area chart
#         area_plot = uh.create_area_chart(network=area_network, variable=variable)
#         third_plot = area_plot

#     # Return the figures, styles and location
#     # plots_style = basic_style
#     return (first_plot, second_plot, third_plot, current_location)

# @app.callback(
#     Output("traffic-one", "clickData"),
#     [
#         Input("reset-traffic-location", "n_clicks"),
#     ],
# )
# def reset_traffic_location(reset):
#     return None

# @app.callback(
#     Output("air quality-one", "figure"),
#     Output("air quality-two", "figure"),
#     Output("air quality-three", "figure"),
#     Output("air quality-location-text", "children"),
#     # Output("results-plots-content", "style"),
#     [
#         Input("crossfilter-season", "value"),
#         Input("crossfilter-time", "value"),
#         Input("crossfilter-area", "value"),
#         Input("crossfilter-demand", "value"),
#         Input("traffic-priority", "value"),
#         Input("crossfilter-air quality-situation", "value"),
#         Input("crossfilter-air quality-variable", "value"),
#         Input("crossfilter-timeline-type", "value"),
#         Input("crossfilter-timestep-range", "value"),
#         Input("air quality-one", "clickData"),
#     ],
# )
# def update_air_quality_graphs(
#     season,
#     time,
#     area,
#     demand,
#     traffic_priority,
#     situation,
#     variable,
#     timeline_type,
#     timestep_range,
#     spatial_click_data,
# ):
#     # Initialize output
#     first_plot = {}
#     second_plot = {}
#     third_plot = {}
#     current_location = ""

#     # Get data
#     network = uh.get_data(
#         area=area,
#         season=season,
#         time=time,
#         demand=demand,
#         optimization=traffic_priority,
#         situation=situation,
#         variable=variable,
#     )
#     network = uh.new_timeline(network=network, timestep_range=timestep_range)
#     network, current_location = uh.spatial_scope(spatial_click_data, network)

#     # Heatmap + bar plot + area chart
#     # Calculate the data
#     heatmap_network = (
#         network.groupby(["Timestep", "Edge"], observed=False)
#         .agg(
#             {
#                 variable: timeline_type,
#                 "Longitude": "first",
#                 "Latitude": "first",
#                 "Name": "first",
#                 "Mobility flow": "sum",
#             }
#         )
#         .reset_index()
#     )
#     # Draw the heatmap
#     heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
#     first_plot = heatmap

#     # Calculate the data
#     barplot_network = (
#         network.groupby(["Mobility mode"], observed=False)
#         .agg({variable: "sum", "Mobility flow": "sum"})
#         .reset_index()
#     )
#     barplot_network["Vehicle average"] = np.round(
#         barplot_network[variable] / barplot_network["Mobility flow"], 4
#     )
#     # Draw the bar plot
#     bar_plot = uh.create_mobility_mode_avg_bar_plot(
#         network=barplot_network, variable=variable
#     )
#     # Output the plot
#     second_plot = bar_plot

#     # Calculate the data
#     area_network = (
#         network.groupby(["Mobility mode", "Timestep"], observed=False)
#         .agg(
#             {
#                 variable: timeline_type,
#                 "Mobility flow": timeline_type,
#             }
#         )
#         .reset_index()
#     )
#     # Draw the area chart
#     area_plot = uh.create_area_chart(network=area_network, variable=variable)
#     # Output the plot
#     third_plot = area_plot

#     # Return the figures, styles and location
#     # plots_style = basic_style
#     return (first_plot, second_plot, third_plot, current_location)

# @app.callback(
#     Output("air quality-one", "clickData"),
#     [Input("reset-air quality-location", "n_clicks")],
# )
# def reset_air_quality_location(reset):
#     return None

# @app.callback(
#     Output("liv-one", "figure"),
#     Output("liv-one", "style"),
#     # Output("liv-two", "figure"),
#     # Output("liv-one", "style"),
#     # Output("liv-location-text", "children"),
#     [
#         Input("crossfilter-area", "value"),
#         Input("crossfilter-situation-liv", "value"),
#         # Input("liv-one", "clickData"),
#     ],
#     # [State("liv-location-text", "children")],
# )
# def update_livability_graphs(
#     area,
#     situation,
#     # spatial_click_data,
#     # current_location,
# ):
#     # TODO
#     pass
