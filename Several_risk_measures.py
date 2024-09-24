#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:21:23 2024

@author: arjunchandranunni
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 10:48:04 2024

@author: arjunchandranunni
"""
import pandas as pd
import matplotlib.pyplot as plt
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


port = rp.Portfolio(returns=X)
method_mu='hist' # Method to estimate expected returns based on historical data.
method_cov='hist' # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model='Classic'

obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True # Use historical scenarios for risk measures that depend on scenarios
rf = 0 # Risk free rate
l = 0 # Risk aversion factor, only useful when obj is 'Utility'
#%%
# Risk Measures available:
#
# 'MV': Standard Deviation.
# 'MAD': Mean Absolute Deviation.
# 'MSV': Semi Standard Deviation.
# 'FLPM': First Lower Partial Moment (Omega Ratio).
# 'SLPM': Second Lower Partial Moment (Sortino Ratio).
# 'CVaR': Conditional Value at Risk.
# 'EVaR': Entropic Value at Risk.
# 'WR': Worst Realization (Minimax)
# 'MDD': Maximum Drawdown of uncompounded cumulative returns (Calmar Ratio).
# 'ADD': Average Drawdown of uncompounded cumulative returns.
# 'CDaR': Conditional Drawdown at Risk of uncompounded cumulative returns.
# 'EDaR': Entropic Drawdown at Risk of uncompounded cumulative returns.
# 'UCI': Ulcer Index of uncompounded cumulative returns.

rms = ['MV', 'MAD', 'MSV', 'FLPM', 'SLPM', 'CVaR',
       'EVaR', 'WR', 'MDD', 'ADD', 'CDaR', 'UCI', 'EDaR']

w_s = pd.DataFrame([])

for i in rms:
    w = port.optimization(model=model, rm=i, obj=obj, rf=rf, l=l, hist=hist)
    w_s = pd.concat([w_s, w], axis=1)
    
w_s.columns = rms

#%%
w_s.style.format("{:.2%}").background_gradient(cmap='YlGn')
#%%

# Plotting a comparison of assets weights for each portfolio

fig = plt.gcf()
fig.set_figwidth(14)
fig.set_figheight(6)
ax = fig.subplots(nrows=1, ncols=1)

w_s.plot.bar(ax=ax)

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

model = 'Classic'
rm = 'MV'
obj = 'Sharpe'
rf = 0

w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

display(w.T)
#%%
ax = rp.plot_pie(w=w, title='Sharpe Mean Variance', others=0.05, nrow=25, cmap = "tab20",
                 height=6, width=10, ax=None)
