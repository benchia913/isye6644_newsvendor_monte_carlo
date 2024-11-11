import ipywidgets as ipw
from UI_constants import *

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
    value=0, 
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
    value=0, 
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


# assemble main widget object
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
                ])
            ])

