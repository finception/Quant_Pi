#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 10:48:04 2024

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
rm = 'CVaR' # Risk measure used, this time will be variance
obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'


#%%

asset_classes = {
    'Assets': ['I-GOLD', 'MPROPDV', 'MS-50', 'MFCSCSH', 'MFCMGOV', 'URTH', 'IEMG', 'QQQ', 'BND', 'EMB', 'RWO'],
    'Industry': ['Gold ETF', 'Thai REIT', 'Thai stocks', 'Thai Bonds', 'Thai money market', 'World index', 'Emerging world', 'NASDAQ', 'American bond', 'Emerging markets bond', 'World REIT']
}

#%%
asset_classes = pd.DataFrame(asset_classes)
asset_classes = asset_classes.sort_values(by=['Assets'])

constraints = {
    'Disabled': [False, False, False, False, False],
    'Type': ['All Assets', 'Classes', 'Classes', 'Classes', 'Classes'],
    'Set': ['', 'Industry', 'Industry', 'Industry', 'Industry'],
    'Position': ['', 'Financials', 'Utilities', 'Industrials', 'Consumer Discretionary'],
    'Sign': ['<=', '<=', '<=', '<=', '<='],
    'Weight': [0.10, 0.2, 0.2, 0.2, 0.2],
    'Type Relative': ['', '', '', '', ''],
    'Relative Set': ['', '', '', '', ''],
    'Relative': ['', '', '', '', ''],
    'Factor': ['', '', '', '', '']
}



constraints = pd.DataFrame(constraints)

display(constraints)

#%%
A, B = rp.assets_constraints(constraints, asset_classes)

#%%%
port.ainequality = A
port.binequality = B


w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

display(w.T)
#%%
ax = rp.plot_pie(w=w, title='CVaR', others=0.05, nrow=25, cmap = "tab20",
                 height=6, width=10, ax=None)
#%%
w_classes = pd.concat([asset_classes.set_index('Assets'), w], axis=1)

display(w_classes)
#%%
w_classes = w_classes.groupby(['Industry']).sum()

display(w_classes)

#%%
ax = rp.plot_pie(w=w_classes, title='Sharpe CVaR', others=0.05, nrow=25,
                 cmap = "tab20", height=6, width=10, ax=None)
#%%


