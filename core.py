# This file holds the core data object

import numpy as np
from scipy.stats import norm
import math

class NewsVendorData():

    def __init__(self):
        self.input_params = \
            {'random_seed': None, 
             'num_iterations': None, 
             'demand_dist_type': None, 
             'demand_unif_min': None, 
             'demand_unif_max': None, 
             'demand_norm_mean': None, 
             'demand_norm_sd': None, 
             'unit_cost': None, 
             'unit_sale_price': None, 
             'unit_salvage_value': None, 
             'order_quantity': None
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

        # compute critical fractile
        unit_overage_cost = self.input_params['unit_cost'] - self.input_params['unit_salvage_value']
        unit_underage_cost = self.input_params['unit_sale_price'] - self.input_params['unit_cost']

        try: 
            self.critical_fractile = unit_underage_cost / (unit_underage_cost + unit_overage_cost)
        # in case of ZeroDivisionError
        except:
            self.critical_fractile = None

        if self.input_params['demand_dist_type'] == 'Uniform':
            self.critical_fractile_order_qty = \
                self.input_params['demand_unif_min'] \
                + (self.input_params['demand_unif_max'] - self.input_params['demand_unif_min']) \
                * self.critical_fractile
            
        if self.input_params['demand_dist_type'] == 'Normal':
            self.critical_fractile_order_qty = \
                self.input_params['demand_norm_mean'] \
                + norm.ppf(self.critical_fractile) * self.input_params['demand_norm_sd']
            
        self.critical_fractile_order_qty = math.ceil(self.critical_fractile_order_qty)

    def generate_demand(self):
        '''
        This method generates a random sample from a normal distribution with mean of demand_mean
        and standard deviation of demand_sd.
        '''

        # set random seed for replicability
        np.random.seed(self.input_params['random_seed'])

        if self.input_params['demand_dist_type'] == 'Uniform':
            self.sample_demand = np.random.uniform(low=self.input_params['demand_unif_min'], 
                                                   high=self.input_params['demand_unif_max'], 
                                                   size=self.input_params['num_iterations'])

        if self.input_params['demand_dist_type'] == 'Normal':
            self.sample_demand = np.random.normal(loc=self.input_params['demand_norm_mean'],
                                                scale=self.input_params['demand_norm_sd'],
                                                size=self.input_params['num_iterations']
                                                )            
        
    def compute_profit_loss(self):
        '''
        This method calculates the profit or loss using the sample_demand attribute.
        '''

        # helper function to calculate PnL given demand
        def helper_compute_profit_loss(demand):

            gross_profit = \
                (self.input_params['unit_sale_price'] - self.input_params['unit_cost']) \
                * np.fmin(self.input_params['order_quantity'], demand)
            
            overage_cost = \
                (self.input_params['unit_cost'] - self.input_params['unit_salvage_value']) \
                * np.fmax(0, self.input_params['order_quantity'] - demand)
            
            underage_cost = \
                (self.input_params['unit_sale_price'] - self.input_params['unit_cost']) \
                * np.fmax(0, demand - self.input_params['order_quantity'])
            
            return (gross_profit - overage_cost - underage_cost)
        
        self.profit_loss = helper_compute_profit_loss(self.sample_demand)

    
    def simulate_order_quantity(self):
        '''
        This method simulates and collects average PnL across all iterations at different order 
        quantities. 
        '''

        if self.input_params['demand_dist_type'] == 'Uniform':
            # simulate min to max
            min_order_qty = int(self.input_params['demand_unif_min'])
            max_order_qty = int(self.input_params['demand_unif_max'])

        if self.input_params['demand_dist_type'] == 'Normal':
            # simulate plus minus 3 SDs
            min_order_qty = \
                int(self.input_params['demand_norm_mean'] - 3 * self.input_params['demand_norm_sd']) 
            max_order_qty = \
                int(self.input_params['demand_norm_mean'] + 3 * self.input_params['demand_norm_sd'])
            

        self.test_order_quantities = list(range(min_order_qty, 
                                                max_order_qty + 1, 
                                                1)
                                        )
        
        # store original order quantity before iteration start
        temp_order_qty = self.input_params['order_quantity']
        
        self.test_average_pnl = []
        
        for order_qty in self.test_order_quantities:
            self.input_params['order_quantity'] = order_qty
            self.compute_profit_loss()
            self.test_average_pnl.append(np.average(self.profit_loss))

        # restore original order quantity in widget and 
        self.input_params['order_quantity'] = temp_order_qty
        self.compute_profit_loss()

        

        
            







##############
# REFERENCES #
##############
# introduction to newsvendor problem - https://www.columbia.edu/~gmg2/4000/pdf/lect_07.pdf   
# wiki page newsvendor problemn - https://en.wikipedia.org/wiki/Newsvendor_model  
# approaches to negative numbers - https://ideas.repec.org/p/pra/mprapa/31842.html  
# Monte Carlo implementation -  chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://dc.etsu.edu/cgi/viewcontent.cgi?article=4522&context=etd








    

    






    

    