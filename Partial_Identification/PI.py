# coding: utf-8

import pandas as pd

class BasePI():
    """Base class of partial identification."""
    def __init__(self, y_name, z_name, df:pd.DataFrame):
        self.y_name = y_name
        self.z_name = z_name
        self.df = df

        self.max_y = self.df[self.y_name].max()
        self.min_y = self.df[self.y_name].min()

    def naive_est(self, z_name):
        """Simplest estimation of causal impacts
        
        """
        for v in self.__dict__.keys():
            if v  not in self.df.columns:
                raise Exception("target or treatment variable is not included in DataFrame")
                
        # CODE HERE
        return self.bound_ate()
    
    def bound_ate(self):
        """calculate min of E[y(1)] - max of E[y(0)] < E[y(1) - y(0)] < max of E[y(1)] - min of E[y(0)] """
        lb_0, ub_0, lb_1, ub_1 =  self.y_of_z(0), self.y_of_z(1)
        lb_effect = lb_1 - ub_0
        ub_effect = ub_1 - lb_0
        return [lb_effect, ub_effect]
        
    def y_of_z(self, t):
        """min of E[y(z=t)] < E[y(z=t)] < max E[y(z=t)] 
        
        This code does'nt work. getitem() could not take an argument like "not t"  
        """
        # min of E[y(z=t)]
        l_bound = self.conditional_mean(t)*self.prob_z[t] + self.min_y*self.prob_z[not t]
        u_bound = self.conditional_mean(t)*self.prob_z[t] + self.max_y*self.prob_z[not t]
        return [l_bound, u_bound]
    @property
    def prob_z(self):
        """probability distribution of discrete variable z
        return: dict whose key is z value and value is prob.
        """
        total_count = self.df.shape[0]
        hist_series = self.df[self.z_name].value_counts() / total_count
        # pd Series to dict
        return hist_series.to_dict()
    def conditional_mean(self, z):
        return self.df.loc[self.df[self.z_name] == z, self.y_name].mean()