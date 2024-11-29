import ipywidgets as ipw
from pprint import pprint
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform, lognorm
import statistics
import numpy as np

from UI_constants import *
from core import NewsVendorData


###########
# MAIN UI #
###########

# application name

w_header_app = ipw.HTML(
    value='''
<b><u>Newsvendor Monte Carlo Application</u></b><br>
<b>Instructions:</b><br>
1. Input parameters.<br>
2. Use any of the following buttons to perform their respective functions:<br>
--> <b>'Generate and Plot Demand':</b> Generates sample demand and plots probability distrbition.<br>
--> <b>'Calculate and Plot P&L':</b> Based on sample demand generated, calculates profit (less overage 
and underage costs) based on given 'Order Quantity'<br>
--> <b>'Find Optimal Order Quantity':</b> Simulates and calculates average profit for different order 
quantities to find the optimal order quantity.<br>
3. View output in the Output Logs section and use 'Clear Output' button to clear output area.<br>
<br>
<b>Assumptions</b><br>
1. Assume demand distribution parameters are known.<br>
2. Allow occurence of negative values for demand. No truncation at 0 or resampling of demand for negative 
demands.<br>
3. Assume single period inventory model, where goods are perishable and salvaged/disposed of at the end 
of each day.<br>
<br>
'''
)


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

w_demand_distribution_type = ipw.Dropdown(
    options=['Uniform', 'Normal'],
    value='Uniform',
    description='Demand Distribution:',
    disabled=False,
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unif_dist_demand_min = ipw.FloatText(
    value=25.0, 
    description='Min: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unif_dist_demand_max = ipw.FloatText(
    value=75.0, 
    description='Max: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_norm_dist_demand_mean = ipw.FloatText(
    value=50.0, 
    description='Mean: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_norm_dist_demand_std_dev = ipw.FloatText(
    value=10.0, 
    description='Standard Deviation: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

demand_dist_handler_dict = \
    {'Uniform': [w_unif_dist_demand_min, w_unif_dist_demand_max],
     'Normal': [w_norm_dist_demand_mean, w_norm_dist_demand_std_dev], 
    #  'Lognormal': [w_lognorm_dist_demand_mean, w_lognorm_dist_demand_sigma]
     }

w_demand_dist_params = ipw.VBox([w_header_demand_dist, w_demand_distribution_type] + 
                                demand_dist_handler_dict[w_demand_distribution_type.value], 
                                layout=CONTAINER_LAYOUT)

# input box 3 - Unit Economics

w_header_unit_economics = ipw.HTML(
    value='<b><u>Unit Economics</b></u>'
)

w_unit_sale_price = ipw.IntText(
    value=10, 
    description='Unit Sale Price: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unit_cost = ipw.IntText(
    value=5, 
    description='Unit Cost: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)

w_unit_salvage_value = ipw.IntText(
    value=3, 
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
    value=50, 
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

# update demand distribution input widgets based on distribution selected
def on_change_demand_dist_widgets(change):
    if change['type'] == 'change' and change['name'] == 'value': 
        w_main_UI.children[1].children[1].children \
        = [w_header_demand_dist, w_demand_distribution_type] \
        + demand_dist_handler_dict[w_demand_distribution_type.value]

w_demand_distribution_type.observe(on_change_demand_dist_widgets)

# button to update class object with input params
w_load_input_params_button = ipw.Button(description='Load Input Params',
                                        button_style='info')

# load params helper function
def load_params():
    global news_vendor_data_object

    news_vendor_data_object.load_params(
        {'random_seed': w_random_seed, 
        'num_iterations': w_num_iterations, 
        'demand_dist_type': w_demand_distribution_type, 
        'demand_unif_min': w_unif_dist_demand_min, 
        'demand_unif_max': w_unif_dist_demand_max, 
        'demand_norm_mean': w_norm_dist_demand_mean, 
        'demand_norm_sd': w_norm_dist_demand_std_dev, 
        'unit_sale_price': w_unit_sale_price,
        'unit_cost': w_unit_cost, 
        'unit_salvage_value': w_unit_salvage_value, 
        'order_quantity': w_order_quantity
        }
    )

    # show params successfully loaded
    with w_output_logs:
        print('Running with the following input params:')
        pprint(news_vendor_data_object.input_params)
        print('\n')
        print(f'Critical fractile = {round(news_vendor_data_object.critical_fractile, 4)}')
        print(f'Theoretical optimal order quantity = {news_vendor_data_object.critical_fractile_order_qty}')

# button to generate demand random variables and scatter plot

w_generate_and_plot_demand_button = ipw.Button(description='Generate and Plot Demand',
                                                button_style='info', 
                                                layout=BUTTON_LAYOUT)

def click_w_generate_and_plot_demand(button):
    global news_vendor_data_object

    # load / refresh input params into core object using widget values
    load_params()

    # generate demand random variables
    news_vendor_data_object.generate_demand()

    # plot distribution on histogram
    fig, ax = plt.subplots()
    num_bins = 100
    ax.hist(x=news_vendor_data_object.sample_demand,
            bins=num_bins, 
            density=True)
    
    # fit best fit line to the data
    if news_vendor_data_object.input_params['demand_dist_type'] == 'Uniform':           
        xmin = news_vendor_data_object.input_params['demand_unif_min'] + (1 / num_bins / 2) # recenter
        xmax = news_vendor_data_object.input_params['demand_unif_max'] - (1 / num_bins / 2) # recenter
        x = np.linspace(xmin, xmax, num_bins)
        bin_length = np.average(np.diff(x))
        y = np.full(shape=x.shape, 
                    fill_value=1.00 / ((num_bins) * bin_length)
                    )
        ax.plot(x, y)

    if news_vendor_data_object.input_params['demand_dist_type'] == 'Normal':           
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 1000)
        mu, std = norm.fit(news_vendor_data_object.sample_demand)
        y = norm.pdf(x, mu, std)
        ax.plot(x, y)

    with w_output_logs:
        plt.show()

w_generate_and_plot_demand_button.on_click(click_w_generate_and_plot_demand)

# button to generate profit and loss distribution

w_generate_and_plot_pnl_button = ipw.Button(description='Calculate and Plot P&L',
                                            button_style='info', 
                                            layout=BUTTON_LAYOUT)

def click_w_generate_and_plot_pnl_button(button):
    global news_vendor_data_object

    # load / refresh input params into core object using widget values
    load_params()

    # generate demand random variables
    news_vendor_data_object.generate_demand()

    # generate demand random variables
    news_vendor_data_object.compute_profit_loss()

    # plot distribution on histogram
    fig, ax = plt.subplots()
    num_bins = 100
    ax.hist(x=news_vendor_data_object.profit_loss,
            bins=num_bins, 
            density=True)
    
    with w_output_logs:
        plt.show()
        # print expected PnL
        average_pnl = np.average(news_vendor_data_object.profit_loss)
        average_pnl = round(average_pnl, 0)
        print(f'Average PnL across all daily demand: ${average_pnl}.')

w_generate_and_plot_pnl_button.on_click(click_w_generate_and_plot_pnl_button)

# button to simulate average PnL at different order quantities and find optimal order qty

w_find_optimal_order_qty_button = ipw.Button(description='Find Optimal Order Quantity',
                                            button_style='success', 
                                            layout=BUTTON_LAYOUT)

def click_w_find_optimal_order_qty_button(button):
    global news_vendor_data_object

    # load / refresh input params into core object using widget values
    load_params()

    # generate demand random variables
    news_vendor_data_object.generate_demand()

    # simulate average PnL at different order quantity
    news_vendor_data_object.simulate_order_quantity()

    # plot average PnL against order quantity
    fig, ax = plt.subplots()

    ax.scatter(np.array(news_vendor_data_object.test_order_quantities),
                np.array(news_vendor_data_object.test_average_pnl), 
                s=15, marker='x')
    
    ymax = max(news_vendor_data_object.test_average_pnl)
    ymin = min(news_vendor_data_object.test_average_pnl)
    xpos = news_vendor_data_object.test_average_pnl.index(ymax)
    xmax = news_vendor_data_object.test_order_quantities[xpos]

    cf_x = news_vendor_data_object.critical_fractile_order_qty
    cf_ypos = news_vendor_data_object.test_order_quantities.index(cf_x)
    cf_y = news_vendor_data_object.test_average_pnl[cf_ypos]

    plt.ylim(ymin, ymax * 1.3)

    ax.annotate(f'Optimal order quantity: ({xmax} units, ${round(ymax, 0)})', 
                xy=(xmax, ymax), 
                xytext=(xmax, ymax * 1.2), 
                arrowprops=dict(facecolor='black', 
                                shrink=0.05), 
                bbox=dict(boxstyle='square, pad=0.3', 
                          fc='w', 
                          ec='k'))
    
    # annotate critical fractile theoretical optimal order quantity
    ax.annotate(f'Critical fractile implied: ({cf_x} units, ${round(cf_y, 0)})', 
                xy=(cf_x, cf_y), 
                xytext=(cf_x, cf_y * 0.8), 
                arrowprops=dict(facecolor='black', 
                                shrink=0.05), 
                bbox=dict(boxstyle='square, pad=0.3', 
                          fc='w', 
                          ec='k'))
    
    with w_output_logs:        
        plt.show()

w_find_optimal_order_qty_button.on_click(click_w_find_optimal_order_qty_button)

# button to clear output logs

w_clear_output_logs_button = ipw.Button(description='Clear Output',
                                        button_style='warning')

def click_w_clear_output_logs_button(button):
    w_output_logs.clear_output()
    
w_clear_output_logs_button.on_click(click_w_clear_output_logs_button)




####################################
# Assemble Final UI and Formatting #
####################################

w_main_UI = ipw.VBox([
                w_header_app, 
                ipw.HBox([
                    ipw.VBox([w_header_rv_gen, 
                              w_random_seed, w_num_iterations, ], 
                             layout=CONTAINER_LAYOUT), 
                    w_demand_dist_params, 
                        ]), 
                ipw.HBox([
                    ipw.VBox([w_header_unit_economics, 
                              w_unit_sale_price, w_unit_cost, w_unit_salvage_value, ], 
                             layout=CONTAINER_LAYOUT),  
                    ipw.VBox([w_header_decision_params, 
                              w_order_quantity, ], 
                             layout=CONTAINER_LAYOUT)
                        ]), 
                ipw.HBox([w_generate_and_plot_demand_button, 
                          w_generate_and_plot_pnl_button, 
                          w_find_optimal_order_qty_button]),
                ipw.VBox([
                    w_output_logs_header, 
                    ipw.VBox([w_output_logs],
                             layout=OUTPUT_LOGS_LAYOUT
                            ), 
                    w_clear_output_logs_button
                        ],  
                    layout=CONTAINER_LAYOUT)
                    ])