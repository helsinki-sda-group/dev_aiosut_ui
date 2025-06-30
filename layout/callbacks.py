from dash import Input, Output, State
import utils.helpers as uh
import utils.constants as uc
import layout.components as lc
import pandas as pd
import numpy as np

basic_style = {"paddingTop": "2vh", "paddingBottom": "2vh"}


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
        Output("visualization-info-collapse", "is_open"),
        Input("visualization-info-button", "n_clicks"),
        State("visualization-info-collapse", "is_open"),
    )
    def toggle_visualization_info_collapse(n, is_open):
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

    @app.callback(
        Output("results-tabs-content-1", "children"),
        Input("results-tabs", "value"),
    )
    def render_view_content(tab):
        if tab == lc.OBJECTIVES[0]:
            return lc.tab_layout(objective=lc.OBJECTIVES[0], variables=None)
        elif tab == lc.OBJECTIVES[1]:
            return lc.tab_layout(
                objective=lc.OBJECTIVES[1], variables=uc.TRAFFIC_VARIABLES
            )
        elif tab == lc.OBJECTIVES[2]:
            return lc.tab_layout(objective=lc.OBJECTIVES[2], variables=uc.AQ_VARIABLES)
        elif tab == lc.OBJECTIVES[3]:
            return lc.tab_layout(objective=lc.OBJECTIVES[3], variables=None)

    @app.callback(
        Output("traffic-one", "figure"),
        Output("traffic-two", "figure"),
        Output("traffic-three", "figure"),
        Output("traffic-one", "style"),
        Output("traffic-two", "style"),
        Output("traffic-three", "style"),
        Output("traffic-location-text", "children"),
        [
            Input("crossfilter-area", "value"),
            Input("crossfilter-traffic-situation", "value"),
            Input("crossfilter-traffic-variable", "value"),
            Input("crossfilter-timeline-type", "value"),
            Input("crossfilter-timestep-range", "value"),
            Input("traffic-one", "clickData"),
        ],
        [State("traffic-location-text", "children")],
    )
    def update_traffic_graphs(
        area,
        situation,
        variable,
        timeline_type,
        timestep_range,
        spatial_click_data,
        current_location,
    ):

        if variable in ["Mobility flow"]:
            # Make a copy of the required data for all plots (to avoid changing the simulation output)
            network = uh.get_data(area=area, situation=situation, variable=variable)
            network = uh.new_timeline(network=network, timestep_range=timestep_range)
            network, location = uh.spatial_scope(spatial_click_data, network)
            bounds = uh.map_bounds(network)

            # Calculate data
            heatmap_network = (
                network.groupby(["Timestep", "Edge"], observed=False)
                .agg(
                    {
                        variable: uc.TIMELINE_FUNCTIONS[timeline_type],
                        "Longitude": "first",
                        "Latitude": "first",
                        "Name": "first",
                    }
                )
                .reset_index()
            )
            # Customize legend
            legend_max = (
                1.2 * heatmap_network[heatmap_network[variable] != 0][variable].median()
            )
            # Draw the heatmap
            heatmap = uh.create_heatmap(network=network, variable=variable)
            first_plot = heatmap
            first_plot_style = {"padding-top": "3vh"}

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
            third_plot_style = {"padding-top": "3vh"}

        # Histogram + bar plot
        elif variable in ["Travel time", "Lost time"]:
            # Calculate data
            network = uh.get_data(area=area, situation=situation, variable=variable)

            # Draw the histogram
            histogram = uh.create_mobility_mode_histogram(
                network=network, variable=variable
            )
            second_plot = histogram
            second_plot_style = {"padding-top": "3vh"}

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
            third_plot_style = {"padding-top": "3vh"}

        # Heatmap + bar plot
        elif variable in ["Noise", "Speed"]:
            # Calculate the data
            network = uh.get_data(situation=situation, variable=variable)
            network = uh.new_timeline(network=network, timestep_range=timestep_range)
            network, location = uh.spatial_scope(spatial_click_data, network)

            # Calculate the data
            heatmap_network = (
                network.groupby(["Timestep", "Edge"], observed=False)
                .agg(
                    {
                        variable: uc.TIMELINE_FUNCTIONS[timeline_type],
                        "Longitude": "first",
                        "Latitude": "first",
                        "Name": "first",
                        "Mobility flow": uc.TIMELINE_FUNCTIONS[timeline_type],
                    }
                )
                .reset_index()
            )
            # Draw the heatmap
            heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
            first_plot = heatmap
            first_plot_style = {"padding-top": "3vh"}

            # Calculate the data
            second_network = uh.get_data(situation=situation, variable=variable)
            second_network = uh.new_timeline(
                network=network, timestep_range=timestep_range
            )
            barplot_network = (
                second_network.groupby(["Mobility mode"], observed=False)
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
            second_plot_style = {"padding-top": "3vh"}

            # Calculate the data
            area_network = (
                network.groupby(["Timestep"], observed=False)
                .agg(
                    {
                        variable: uc.TIMELINE_FUNCTIONS[timeline_type],
                        "Mobility flow": uc.TIMELINE_FUNCTIONS[timeline_type],
                    }
                )
                .reset_index()
            )
            # Draw the area chart
            area_plot = uh.create_area_chart(network=area_network, variable=variable)
            third_plot = area_plot
            third_plot_style = {"padding-top": "3vh"}

        # Return the figures, styles and location
        return (
            first_plot,
            first_plot_style,
            second_plot,
            second_plot_style,
            third_plot,
            third_plot_style,
            location,
        )

    @app.callback(
        Output("traffic-one", "clickData"),
        [
            Input("reset-button-traffic", "n_clicks"),
        ],
    )
    def reset_traffic_location(reset):
        return None

    @app.callback(
        Output("aq-one", "figure"),
        Output("aq-one", "style"),
        Output("aq-two", "figure"),
        Output("aq-two", "style"),
        Output("aq-three", "figure"),
        Output("aq-three", "style"),
        Output("aq-location-text", "children"),
        [
            Input("crossfilter-area", "value"),
            Input("crossfilter-situation-aq", "value"),
            Input("crossfilter-variable-aq", "value"),
            Input("crossfilter-timeline-type", "value"),
            Input("crossfilter-timestep-range", "value"),
            Input("aq-one", "clickData"),
        ],
        [State("aq-location-text", "children")],
    )
    def update_air_quality_graphs(
        area,
        situation,
        variable,
        timeline_type,
        timestep_range,
        spatial_click_data,
        current_location,
    ):
        # Make a copy of the initial data (to avoid changing the simulation output)
        network = uh.get_data(area=area, situation=situation, variable=variable)
        network = uh.new_timeline(network=network, timestep_range=timestep_range)
        network, location = uh.spatial_scope(spatial_click_data, network)

        # Heatmap + bar plot + area chart
        # Calculate the data
        heatmap_network = (
            network.groupby(["Timestep", "Edge"], observed=False)
            .agg(
                {
                    variable: uc.TIMELINE_FUNCTIONS[timeline_type],
                    "Longitude": "first",
                    "Latitude": "first",
                    "Name": "first",
                    "Mobility flow": "sum",
                }
            )
            .reset_index()
        )
        # Draw the heatmap
        heatmap = uh.create_heatmap(network=heatmap_network, variable=variable)
        first_plot = heatmap
        first_plot_style = {"padding-top": "3vh"}

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
        second_plot_style = {"padding-top": "3vh"}

        # Calculate the data
        area_network = (
            network.groupby(["Mobility mode", "Timestep"], observed=False)
            .agg(
                {
                    variable: uc.TIMELINE_FUNCTIONS[timeline_type],
                    "Mobility flow": uc.TIMELINE_FUNCTIONS[timeline_type],
                }
            )
            .reset_index()
        )
        # Draw the area chart
        area_plot = uh.create_area_chart(network=area_network, variable=variable)
        # Output the plot
        third_plot = area_plot
        third_plot_style = {"padding-top": "3vh"}

        # Return the figures, styles and location
        return (
            first_plot,
            first_plot_style,
            second_plot,
            second_plot_style,
            third_plot,
            third_plot_style,
            location,
        )

    @app.callback(
        Output("aq-one", "clickData"),
        [Input("reset-button-aq", "n_clicks")],
    )
    def reset_air_quality_location(reset):
        return None

    @app.callback(
        Output("liv-one", "figure"),
        Output("liv-one", "style"),
        # Output("liv-two", "figure"),
        # Output("liv-one", "style"),
        # Output("liv-location-text", "children"),
        [
            Input("crossfilter-area", "value"),
            Input("crossfilter-situation-liv", "value"),
            # Input("liv-one", "clickData"),
        ],
        # [State("liv-location-text", "children")],
    )
    def update_livability_graphs(
        area,
        situation,
        # spatial_click_data,
        # current_location,
    ):
        # TODO
        pass
