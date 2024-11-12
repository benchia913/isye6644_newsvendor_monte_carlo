# This file holds the core data object

import numpy as np

class NewsVendorData():

    def __init__(self):
        self.input_params = \
            {'random_seed': None, 
             'num_iterations': None, 
             'demand_mean': None, 
             'demand_sd': None, 
             'unit_cost': None, 
             'unit_sale_price': None, 
             'unit_salvage_value': None, 
             'unit_order_quantity': None
        }

    def load_params(self, 
                    input_dict_key_to_widget_map: dict
                    ):
        '''
        This method takes in a dictionary with input param dict key: widget pairs to update 
        the input_params attribute of the class object.
        '''

        for key, widget in input_dict_key_to_widget_map.items():
            self.input_params[key] = widget.value

    def generate_demand(self):
        '''
        This method generates a random sample from a normal distribution with mean of demand_mean
        and standard deviation of demand_sd.
        '''

        # set random seed for replicability
        np.random.seed(self.input_params['random_seed'])

        self.sample_demand = np.random.normal(loc=self.input_params['demand_mean'],
                                                scale=self.input_params['demand_sd'],
                                                size=self.input_params['num_iterations']
                                                )
        
        








    

    