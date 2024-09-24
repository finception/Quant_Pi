#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 10:03:18 2024

@author: arjunchandranunni
"""

import pandas as pd
import riskfolio as rp
data11 = pd.read_excel("coreport_11_python.xlsx",sheet_name='Daily_11')

daily_prices=data11.iloc[3:,1:]
daily_prices_rev=daily_prices[::-1].reset_index(drop = True)
daily_prices_rev = daily_prices_rev.drop(daily_prices_rev.index[-1]).reset_index(drop=True)

column_names=['I-GOLD',	'MPROPDV',	'MS-50',	'MFCSCSH',	'MFCMGOV',	'URTH',	'IEMG',	'QQQ',	'BND',	'EMB',	'RWO']

daily_prices_rev.columns=column_names
#%%

monthly_prices=pd.read_excel("coreport_11_python.xlsx",sheet_name='Monthly_11')

#%%

X = daily_prices_rev.pct_change()
X.drop(X.index[0]).reset_index(drop=True)
X=X.dropna()
X=X.reset_index(drop=True)

#%%




# Building the portfolio object
port = rp.Portfolio(returns=X)

# Calculating optimal portfolio

# Select method and estimate input parameters:

method_mu='hist' # Method to estimate expected returns based on historical data.
method_cov='hist' # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = 'MV' # Risk measure used, this time will be variance
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'

w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

display(w.T)
#%%
# Plotting the composition of the portfolio

ax = rp.plot_pie(w=w, title='Sharpe Mean Variance', others=0.05, nrow=25, cmap = "tab20",
                 height=6, width=10, ax=None)

#%%
points = 50 # Number of points of the frontier

frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)

display(frontier.T.head())
#%%
# Plotting the efficient frontier

label = 'Max Risk Adjusted Return Portfolio' # Title of point
mu = port.mu # Expected returns
cov = port.cov # Covariance matrix
returns = port.returns # Returns of the assets

ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm,
                      rf=rf, alpha=0.05, cmap='viridis', w=w, label=label,
                      marker='*', s=16, c='r', height=6, width=10, ax=None)

#%%

# Plotting efficient frontier composition

ax = rp.plot_frontier_area(w_frontier=frontier, cmap="tab20", height=6, width=10, ax=None)

#%%





