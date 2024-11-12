import ipywidgets as ipw
from pprint import pprint
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics
import numpy as np

from UI_constants import *
from core import NewsVendorData

###############
# ASSUMPTIONS #
###############






###########
# MAIN UI #
###########


# input widgets

# input box 1 - Random Variable Generation

w_header_rv_gen = ipw.HTML(
    value='<b><u>Random Variable Generation</u></b>'
)

w_random_seed = ipw.IntText(
    value=1, 
    description='Random Seed: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)


w_num_iterations = ipw.IntText(
    value=100_000, 
    description='Number of Iterations: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

# input box 2 - Demand Distribution

w_header_demand_dist = ipw.HTML(
    value='<b><u>Demand Distribution</b></u>'
)

w_demand_mean = ipw.IntText(
    value=0, 
    description='Demand Mean: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_demand_std_dev = ipw.IntText(
    value=1, 
    description='Demand Standard Deviation: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

# input box 3 - Unit Economics

w_header_unit_economics = ipw.HTML(
    value='<b><u>Unit Economics</b></u>'
)

w_unit_cost = ipw.IntText(
    value=0, 
    description='Unit Cost: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unit_sale_price = ipw.IntText(
    value=0, 
    description='Unit Sale Price: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unit_salvage_value = ipw.IntText(
    value=0, 
    description='Unit Salvage Value: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

# input box 4 - Decision Parameters

w_header_decision_params = ipw.HTML(
    value='<b><u>Decision Parameters</b></u>'
)

w_order_quantity = ipw.IntText(
    value=0, 
    description='Order Quantity: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

# output logs
w_output_logs_header = ipw.HTML(
    value='<b><u>Output Logs:</b></u>'
)

w_output_logs = ipw.Output()



##################################################
# Widget Buttons, Events and Object Statefulness #
##################################################

# initialize main NewsVendorData object which tracks statefulness
news_vendor_data_object = NewsVendorData()

# button to update class object with input params
w_load_input_params_button = ipw.Button(description='Load Input Params',
                                        button_style='info')

def click_w_load_input_params_button(button):
    global news_vendor_data_object

    news_vendor_data_object.load_params(
        {'random_seed': w_random_seed, 
        'num_iterations': w_num_iterations, 
        'demand_mean': w_demand_mean, 
        'demand_sd': w_demand_std_dev, 
        'unit_cost': w_unit_cost, 
        'unit_sale_price': w_unit_sale_price, 
        'unit_salvage_value': w_unit_salvage_value, 
        'unit_order_quantity': w_order_quantity
        }
    )

    # show params successfully loaded
    with w_output_logs:
        print('Input params successfully loaded:')
        pprint(news_vendor_data_object.input_params)

w_load_input_params_button.on_click(click_w_load_input_params_button)

# button to generate demand random variables and scatter plot

w_generate_and_plot_demand_button = ipw.Button(description='Generate Demand',
                                                button_style='success')

def click_w_generate_and_plot_demand(button):
    global news_vendor_data_object

    # generate demand random variables
    news_vendor_data_object.generate_demand()

    # plot distribution on histogram
    fig, ax = plt.subplots()
    ax.hist(x=news_vendor_data_object.sample_demand,
            bins=100, 
            density=True)
    # fit a normal line to the data
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    mu, std = norm.fit(news_vendor_data_object.sample_demand)
    ax.plot(x, norm.pdf(x, mu, std))

    with w_output_logs:
        plt.show()

w_generate_and_plot_demand_button.on_click(click_w_generate_and_plot_demand)




####################################
# Assemble Final UI and Formatting #
####################################

w_main_UI = ipw.VBox([
                ipw.HBox([
                    ipw.VBox([w_header_rv_gen, 
                              w_random_seed, w_num_iterations, ], 
                             layout=CONTAINER_LAYOUT), 
                    ipw.VBox([w_header_demand_dist, 
                              w_demand_mean, w_demand_std_dev, ], 
                             layout=CONTAINER_LAYOUT), 
                ]), 
                ipw.HBox([
                    ipw.VBox([w_header_unit_economics, 
                              w_unit_cost, w_unit_sale_price, w_unit_salvage_value, ], 
                             layout=CONTAINER_LAYOUT),  
                    ipw.VBox([w_header_decision_params, 
                              w_order_quantity, ], 
                             layout=CONTAINER_LAYOUT)
                ]), 
                ipw.HBox([w_load_input_params_button, 
                          w_generate_and_plot_demand_button]),
                ipw.VBox([
                    w_output_logs_header, 
                    ipw.VBox([w_output_logs],
                             layout=OUTPUT_LOGS_LAYOUT
                            )
                        ],  
                    layout=CONTAINER_LAYOUT)
            ])