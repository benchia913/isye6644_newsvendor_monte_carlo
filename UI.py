import ipywidgets as ipw
from UI_constants import *


# input widgets
w_random_seed = ipw.IntText(
    value=0, 
    description='Random Seed: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
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

w_num_iterations = ipw.IntText(
    value=0, 
    description='Number of Iterations: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
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

w_order_quantity = ipw.IntText(
    value=0, 
    description='Demand Mean: ', 
    disabled=False, 
    style=INT_TEXT_STYLE, 
    layout=INT_TEXT_LAYOUT
)


# assemble main widget object
w_main_UI = ipw.VBox([
    w_random_seed, w_num_iterations, 
    w_demand_mean, w_demand_std_dev, 
    w_unit_cost, w_unit_sale_price, w_unit_salvage_value, 
    w_order_quantity, 
    ])

